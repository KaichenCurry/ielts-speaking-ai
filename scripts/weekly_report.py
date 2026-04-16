#!/usr/bin/env python3
"""每周学情分析：从 Notion 作业库提取学生一周数据，生成汇总"""
import sys
import json
import urllib.request
from datetime import datetime, timedelta

NOTION_TOKEN = "YOUR_NOTION_TOKEN"
HOMEWORK_DB = "3412e55d-7136-8179-9ac8-ee60a420ac21"  # 新作业反馈库

def get_text(props, key):
    """从prop提取纯文本"""
    p = props.get(key, {})
    if p.get("type") == "rich_text":
        return "".join([t.get("plain_text","") for t in p.get("rich_text",[])])
    if p.get("type") == "title":
        return "".join([t.get("plain_text","") for t in p.get("title",[])])
    return ""

def get_num(props, key):
    return props.get(key, {}).get("number") or 0

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

def query_student_homework(student_id: str, days: int = 7) -> list:
    """查询指定学生最近 N 天的所有作业"""
    cutoff = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
    url = f"https://api.notion.com/v1/databases/{HOMEWORK_DB}/query"
    payload = {
        "filter": {
            "and": [
                {"property": "学生昵称", "rich_text": {"contains": student_id}},
                {"property": "测评日期", "date": {"on_or_after": cutoff}},
            ]
        },
        "sorts": [{"property": "测评日期", "direction": "ascending"}],
        "page_size": 50
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {NOTION_TOKEN}")
    req.add_header("Notion-Version", "2022-06-28")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as resp:
        results = json.load(resp).get("results", [])

    records = []
    for page in results:
        props = page.get("properties", {})
        page_id = page.get("id", "")
        page_content = get_page_blocks(page_id) if page_id else ""
        records.append({
            "学生昵称": get_text(props, "学生昵称"),
            "快捷ID": get_text(props, "快捷ID"),
            "题目类别": get_text(props, "题目类别"),
            "综合BandScore": get_num(props, "综合BandScore"),
            "Part1均分": get_num(props, "Part1BandScore"),
            "Part2BandScore": get_num(props, "Part2BandScore"),
            "Part3均分": get_num(props, "Part3BandScore"),
            "测评日期": props.get("时间戳", {}).get("date", {}).get("start", ""),
            "page_content": page_content,
        })
    return records

def get_all_student_ids(days: int = 7) -> list:
    """获取所有有作业记录的学生ID"""
    cutoff = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
    url = f"https://api.notion.com/v1/databases/{HOMEWORK_DB}/query"
    payload = {
        "filter": {"property": "测评日期", "date": {"on_or_after": cutoff}},
        "page_size": 100
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {NOTION_TOKEN}")
    req.add_header("Notion-Version", "2022-06-28")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as resp:
        results = json.load(resp).get("results", [])

    ids = set()
    for page in results:
        props = page.get("properties", {})
        sid = get_text(props, "学生昵称")
        if sid:
            ids.add(sid)
    return list(ids)

def generate_student_report(student_id: str, records: list) -> str:
    """为单个学生生成详细周报"""
    if not records:
        return ""

    total = len(records)
    bands = [r["综合BandScore"] for r in records]
    avg_band = sum(bands) / len(bands) if bands else 0

    # 分析各维度问题（从page_content中提取）
    feedback_parts = []
    for r in records:
        content = r.get("page_content", "")
        if content:
            # 截取关键段落
            snippet = content[:200].replace("\n", " ")
            feedback_parts.append(f"【{r['快捷ID']}】Band {r['综合BandScore']} | {snippet}...")

    report = f"""
═══════════════════════════════════════
📊 学生周报 | {student_id}
═══════════════════════════════════════

📈 本周概况
  • 练习次数：{total}次
  • 平均Band：{avg_band:.1f}
  • 最高Band：{max(bands) if bands else 0:.1f}
  • 最低Band：{min(bands) if bands else 0:.1f}

📝 练习详情
"""
    for i, r in enumerate(records, 1):
        report += f"  {i}. 【{r['快捷ID']}】Band {r['综合BandScore']:.1f} | P1:{r['Part1均分']:.1f} P2:{r['Part2BandScore']:.1f} P3:{r['Part3均分']:.1f} ({r['测评日期']})\n"

    if feedback_parts:
        report += "\n💬 反馈摘要\n  " + "\n  ".join(feedback_parts[:5])

    return report

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        # 获取所有学生
        student_ids = get_all_student_ids()
        print(json.dumps({"students": student_ids}, ensure_ascii=False))
    elif len(sys.argv) > 1:
        # 获取指定学生报告
        student_id = sys.argv[1]
        records = query_student_homework(student_id)
        if records:
            report = generate_student_report(student_id, records)
            print(report)
        else:
            print(f"暂无{student_id}的作业记录")
    else:
        print("Usage:")
        print("  weekly_report.py --all          # 列出所有学生")
        print("  weekly_report.py <学生昵称>    # 生成学生周报")
