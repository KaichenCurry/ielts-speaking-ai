#!/usr/bin/env python3
"""
每周学情报告发送器 - 由 crontab 每周五 18:00 EDT 触发
1. 从 Notion 获取所有学生本周作业（通过数据库属性）
2. 读取每个页面的详细 blocks 内容
3. 用 AI 生成深度分析报告
4. 通过 Telegram Bot API 发送到群组
"""
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from collections import defaultdict

# ============ 配置 ============
NOTION_TOKEN = "YOUR_NOTION_TOKEN"
HOMEWORK_DB = "3412e55d-7136-8179-9ac8-ee60a420ac21"  # 作业反馈库
BADCASE_DB = "3412e55d-7136-8113-aa98-cfd36af9799c"
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
GROUP_CHAT_ID = "-5165692087"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
MODEL = "gpt-4o-mini"
# ==============================

def notion_query(db_id: str, sql: dict) -> list:
    url = f"https://api.notion.com/v1/databases/{db_id}/query"
    data = json.dumps(sql).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {NOTION_TOKEN}")
    req.add_header("Notion-Version", "2022-06-28")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.load(resp).get("results", [])
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode()[:200]}", file=sys.stderr)
        return []

def get_page_blocks(page_id: str) -> str:
    """获取页面正文内容（所有block的纯文本）"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Bearer {NOTION_TOKEN}")
    req.add_header("Notion-Version", "2022-06-28")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.load(resp)
            texts = []
            for block in result.get("results", []):
                block_type = block.get("type", "")
                block_data = block.get(block_type, {})
                rich_text = block_data.get("rich_text", [])
                text = "".join([t.get("plain_text", "") for t in rich_text])
                if text.strip():
                    texts.append(text.strip())
            return "\n".join(texts)
    except Exception as e:
        print(f"获取page blocks失败: {e}", file=sys.stderr)
        return ""

def get_student_homework(days: int = 7) -> dict:
    """获取所有学生本周作业"""
    cutoff = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
    payload = {
        "filter": {"property": "测评日期", "date": {"on_or_after": cutoff}},
        "page_size": 100,
        "sorts": [{"property": "测评日期", "direction": "descending"}]
    }
    results = notion_query(HOMEWORK_DB, payload)

    records_by_student = defaultdict(list)
    for page in results:
        props = page.get("properties", {})
        
        # 从数据库属性读取关键数据
        def get_text(key):
            p = props.get(key, {})
            if p.get("type") == "rich_text":
                return "".join([t.get("plain_text", "") for t in p.get("rich_text", [])])
            if p.get("type") == "title":
                return "".join([t.get("plain_text", "") for t in p.get("title", [])])
            if p.get("type") == "select":
                return (p.get("select") or {}).get("name", "")
            return ""
        
        def get_num(key):
            return props.get(key, {}).get("number") or 0
        
        sid = get_text("学生昵称")
        if not sid:
            continue
        
        # 读取页面正文blocks
        page_id = page.get("id", "")
        page_content = get_page_blocks(page_id) if page_id else ""
        
        record = {
            "学生昵称": sid,
            "快捷ID": get_text("快捷ID"),
            "题目类别": get_text("题目类别"),
            "综合Band": get_num("综合Band"),
            "Part1均分": get_num("Part1均分"),
            "Part2Band": get_num("Part2Band"),
            "Part3均分": get_num("Part3均分"),
            "测评日期": props.get("测评日期", {}).get("date", {}).get("start", ""),
            "page_content": page_content,  # 页面正文原文
        }
        records_by_student[sid].append(record)

    return dict(records_by_student)

def get_week_badcases(days: int = 7) -> list:
    """获取本周错题本数据"""
    cutoff = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
    payload = {
        "filter": {"property": "测评日期", "date": {"on_or_after": cutoff}},
        "page_size": 50
    }
    results = notion_query(BADCASE_DB, payload)

    badcases = []
    for page in results:
        props = page.get("properties", {})
        def get_text(key):
            p = props.get(key, {})
            if p.get("type") == "rich_text":
                return "".join([t.get("plain_text", "") for t in p.get("rich_text", [])])
            if p.get("type") == "title":
                return "".join([t.get("plain_text", "") for t in p.get("title", [])])
            return ""
        def get_num(key):
            return props.get(key, {}).get("number") or 0
        
        badcases.append({
            "学生ID": get_text("学生ID"),
            "原始题目": get_text("原始题目"),
            "错误类型": get_text("错误类型"),
            "老师正确纠正": get_text("老师正确纠正"),
            "最终BandScore": get_num("最终BandScore"),
            "测评日期": props.get("时间戳", {}).get("date", {}).get("start", ""),
        })
    return badcases

def ai_analyze_week(student_id: str, records: list, all_content: str, badcases: list) -> str:
    """调用 AI 生成深度周报分析"""
    if not records:
        return ""
    
    # 构建prompt
    total = len(records)
    bands = [r["综合Band"] for r in records]
    avg_band = sum(bands) / len(bands) if bands else 0
    
    # 提取本周各维度错误
    error_grammar, error_vocab, error_tense, error_logic, error_ideas = [], [], [], [], []
    
    for r in records:
        content = r.get("page_content", "")
        lines = content.split("\n")
        for line in lines:
            lt = line.lower()
            if "语法" in line and ("❌" in line or "错误" in line):
                error_grammar.append(line[:100])
            elif "词汇" in line and ("❌" in line or "错误" in line):
                error_vocab.append(line[:100])
            elif "时态" in line and ("❌" in line or "错误" in line):
                error_tense.append(line[:100])
            elif "逻辑" in line and ("❌" in line or "⚠️" in line):
                error_logic.append(line[:100])
            elif "思路" in line and ("❌" in line or "⚠️" in line):
                error_ideas.append(line[:100])
    
    prompt = f"""你是雅思口语教学助手，生成本周深度学情报告。

## 学生信息
学生：{student_id}
本周练习：{total}次
平均Band：{avg_band:.1f}
Band范围：{min(bands) if bands else 0:.1f} ~ {max(bands) if bands else 0:.1f}

## 各次练习Band
{chr(10).join([f"- {r['快捷ID']} | P1:{r['Part1均分']} P2:{r['Part2Band']} P3:{r['Part3均分']} 综合:{r['综合Band']}" for r in records])}

## 本周错误记录（从作业反馈中提取）
语法错误（{len(error_grammar)}次）：
{chr(10).join(error_grammar[:5]) if error_grammar else "无明显语法错误"}

词汇错误（{len(error_vocab)}次）：
{chr(10).join(error_vocab[:5]) if error_vocab else "无明显词汇错误"}

时态错误（{len(error_tense)}次）：
{chr(10).join(error_tense[:5]) if error_tense else "无明显时态错误"}

逻辑问题（{len(error_logic)}次）：
{chr(10).join(error_logic[:5]) if error_logic else "无明显逻辑问题"}

思路问题（{len(error_ideas)}次）：
{chr(10).join(error_ideas[:5]) if error_ideas else "无明显思路问题"}

## 本周错题纠正（{len(badcases)}条）
{chr(10).join([f"- {bc['错误类型']}: {bc['老师正确纠正'][:80]}" for bc in badcases[:3]]) if badcases else "本周无错题纠正"}

## 产出要求
生成一份深度周报，包含：
1. **本周表现综述**（1-2句）
2. **各维度详细分析**（语法/词汇/时态/逻辑/思路，每个维度2-3句话）
3. **最需突破的1-2个具体问题**（给出具体例子和改进建议）
4. **下周练习重点**（1-2条具体可行的建议）

注意：只基于以上真实数据，不要编造内容。如果某维度表现良好，明确指出哪里做得好。"""

    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {OPENAI_API_KEY}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.load(resp)
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"AI分析失败: {e}", file=sys.stderr)
        return ""

def analyze_band_trend(records: list) -> dict:
    """分析Band分数趋势"""
    if not records:
        return {}
    sorted_records = sorted(records, key=lambda x: x.get("测评日期", ""))
    bands = [r["综合Band"] for r in sorted_records]
    if len(bands) < 2:
        return {"trend": "→ 首次练习", "change": 0}
    
    first_half = bands[:len(bands)//2]
    second_half = bands[len(bands)//2:]
    first_avg = sum(first_half) / len(first_half)
    second_avg = sum(second_half) / len(second_half)
    
    change = second_avg - first_avg
    if change >= 0.3:
        trend = "📈 上升"
    elif change <= -0.3:
        trend = "📉 下降"
    else:
        trend = "→ 持平"
    
    return {"avg": sum(bands)/len(bands), "trend": trend, "change": round(change, 2)}

def telegram_send(text: str) -> bool:
    """发送Telegram消息"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": GROUP_CHAT_ID, "text": text, "parse_mode": "HTML"}
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.load(resp)
            return result.get("ok", False)
    except Exception as e:
        print(f"Telegram发送失败: {e}", file=sys.stderr)
        return False

def generate_weekly_report(student_records: dict, badcases: list) -> str:
    """生成完整周报"""
    if not student_records:
        return ""

    # 全局统计
    total_students = len(student_records)
    total_homework = sum(len(recs) for recs in student_records.values())
    all_bands = [r["综合Band"] for recs in student_records.values() for r in recs]
    avg_band = sum(all_bands) / len(all_bands) if all_bands else 0

    # Band分布
    band_ranges = {
        "8.0+": len([b for b in all_bands if b >= 8.0]),
        "7.0-7.9": len([b for b in all_bands if 7.0 <= b < 8.0]),
        "6.0-6.9": len([b for b in all_bands if 6.0 <= b < 7.0]),
        "5.0-5.9": len([b for b in all_bands if 5.0 <= b < 6.0]),
        "<5.0": len([b for b in all_bands if b < 5.0]),
    }

    # 学生排名
    student_stats = [(sid, len(recs), sum(r["综合Band"] for r in recs)/len(recs)) 
                     for sid, recs in student_records.items()]
    student_stats.sort(key=lambda x: x[2], reverse=True)

    # 构建报告
    lines = []
    lines.append("📊 ════════════════════════════════════ 📊")
    lines.append(f"       雅思口语个性化反馈周报")
    lines.append(f"         {datetime.now().strftime('%Y-%m-%d')}")
    lines.append("📊 ════════════════════════════════════ 📊")
    lines.append("")
    lines.append(f"🏆 班级概况：{total_students}人练习，共{total_homework}次，平均Band {avg_band:.1f}")
    
    # Band分布
    lines.append("")
    lines.append("📈 Band分布")
    for rng, cnt in band_ranges.items():
        bar = "█" * cnt + "░" * max(0, 8 - cnt)
        lines.append(f"   {rng:>7}: {bar} {cnt}人")

    # 排名
    lines.append("")
    lines.append("🌟 最佳表现 TOP3")
    for i, (sid, cnt, avg) in enumerate(student_stats[:3], 1):
        medal = ["🥇", "🥈", "🥉"][i-1]
        trend_data = analyze_band_trend(student_records[sid])
        lines.append(f"   {medal} {sid}: {avg:.1f} ({cnt}次) {trend_data['trend']}")

    # 每个人深度分析
    lines.append("")
    lines.append("═══ 深度分析 ═══")
    
    # 按平均Band排序取前几名和后几名
    focus = student_stats[:3] + (student_stats[-2:] if len(student_stats) > 4 else [])
    focus = sorted({(s[0], s) for s in focus}, key=lambda x: x[1][2], reverse=True)
    
    for sid, cnt, avg in [x[1] for x in focus]:
        records = student_records[sid]
        trend_data = analyze_band_trend(records)
        student_badcases = [bc for bc in badcases if bc.get("学生ID") == sid]
        
        lines.append("")
        lines.append(f"─── {sid} ───")
        lines.append(f"   练习{cnt}次 | 均Band {avg:.1f} | {trend_data['trend']}")
        
        # AI深度分析
        all_content = "\n".join([r.get("page_content", "") for r in records])
        ai_analysis = ai_analyze_week(sid, records, all_content, student_badcases)
        if ai_analysis:
            for line in ai_analysis.strip().split("\n"):
                if line.strip():
                    lines.append(f"   {line.strip()}")
        else:
            # 兜底：简单统计
            p1_avg = sum(r["Part1均分"] for r in records) / len(records)
            p2_avg = sum(r["Part2Band"] for r in records) / len(records)
            p3_avg = sum(r["Part3均分"] for r in records) / len(records)
            lines.append(f"   P1:{p1_avg:.1f} P2:{p2_avg:.1f} P3:{p3_avg:.1f}")

    # 本周错题汇总
    if badcases:
        lines.append("")
        lines.append("═══ 本周错题纠正 ═══")
        for bc in badcases[:5]:
            lines.append(f"   • [{bc.get('错误类型','未知')}] {bc.get('原始题目','')[:30]}")
            lines.append(f"     → {bc.get('老师正确纠正','')[:60]}")

    lines.append("")
    lines.append("🐉 AI雅思助手 | 反馈维度：语法 | 词汇 | 时态 | 逻辑 | 思路")

    return "\n".join(lines)

if __name__ == "__main__":
    print(f"[{datetime.now().isoformat()}] 开始生成周报...")

    student_records = get_student_homework(days=7)
    print(f"发现 {len(student_records)} 个学生有作业")

    if not student_records:
        print("本周无作业，跳过发送")
        sys.exit(0)

    badcases = get_week_badcases(days=7)
    print(f"本周错题纠正: {len(badcases)}条")

    report = generate_weekly_report(student_records, badcases)

    ok = telegram_send(report)
    print(f"发送{'成功 ✅' if ok else '失败 ❌'}")
    print(f"\n[{datetime.now().isoformat()}] 周报发送完成")
