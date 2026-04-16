#!/usr/bin/env python3
"""
追加作业记录到 Notion 作业反馈库（精简版）
每个问题尽量用1个block存储逐句诊断，控制总block在100以内
"""
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime

NOTION_TOKEN = "YOUR_NOTION_TOKEN"
DB_ID = "3412e55d-7136-8179-9ac8-ee60a420ac21"


def create_homework_v2(data: dict) -> str:
    """
    创建作业反馈页面 - 精简版
    逐句诊断合并到单行中，减少block数量
    """
    display_name = f"{data['student_nickname']} - {data['topic_short_id']} - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    eval_data = data.get('evaluation', {})
    scores = data.get('scores', {})

    blocks = []

    # ========== 📋 基本信息 ==========
    blocks.append(bh("📋 基本信息"))
    blocks.append(bb(f"学生昵称：{data.get('student_nickname', '')}"))
    blocks.append(bb(f"题目编号：{data.get('topic_short_id', '')} | 类别：{data.get('topic_category', '')}"))
    blocks.append(bb(f"测评时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}"))

    # ========== 📝 Part 1 ==========
    blocks.append(bh("📝 Part 1"))

    part1 = eval_data.get('part1', [])
    for i, q in enumerate(part1, 1):
        blocks.append(bh(f"Q{i}：{q.get('question', '')}", level=3))
        blocks.append(bp(f"【原文】{q.get('transcript', '')}"))
        blocks.append(bp(f"【得分】Band {q.get('band', 'N/A')}"))

        ana = q.get('analysis', {}) or {}
        sentences = ana.get('sentences', [])

        if sentences:
            # 逐句紧凑格式
            sent_lines = []
            for s in sentences:
                sid = s.get('id', 0)
                stext = s.get('text', '')
                diag = s.get('diagnosis', '')
                fix = s.get('fix', '')

                if '✅' in diag:
                    sent_lines.append(f"S{sid}. {stext} → ✅")
                elif fix:
                    sent_lines.append(f"S{sid}. {stext} → {diag} | → {fix}")
                else:
                    sent_lines.append(f"S{sid}. {stext} → {diag}")

            blocks.append(bp("【诊断】" + "｜".join(sent_lines)))

            # 总结
            summary = ana.get('summary', {})
            if summary:
                blocks.append(bp(f"【总结】GRA:{summary.get('grammar','')}｜LR:{summary.get('vocabulary','')}｜FC:{summary.get('logic','')}"))
        else:
            # 旧格式
            blocks.append(bp("【诊断】" + f"GRA:{ana.get('grammar','')}｜LR:{ana.get('vocabulary','')}｜FC:{ana.get('logic','')}"))

    # ========== 📝 Part 2 ==========
    blocks.append(bh("📝 Part 2"))

    part2 = eval_data.get('part2', {})
    if part2:
        blocks.append(bp(f"【原文】{part2.get('transcript', '')}"))
        blocks.append(bp(f"【得分】Band {part2.get('band', 'N/A')}"))

        ana = part2.get('analysis', {}) or {}
        sentences = ana.get('sentences', [])

        if sentences:
            sent_lines = []
            for s in sentences:
                sid = s.get('id', 0)
                stext = s.get('text', '')
                diag = s.get('diagnosis', '')
                fix = s.get('fix', '')

                if '✅' in diag:
                    sent_lines.append(f"S{sid}. {stext} → ✅")
                elif fix:
                    sent_lines.append(f"S{sid}. {stext} → {diag} | → {fix}")
                else:
                    sent_lines.append(f"S{sid}. {stext} → {diag}")

            blocks.append(bp("【诊断】" + "｜".join(sent_lines)))

            summary = ana.get('summary', {})
            if summary:
                blocks.append(bp(f"【总结】GRA:{summary.get('grammar','')}｜LR:{summary.get('vocabulary','')}｜FC:{summary.get('logic','')}"))

    # ========== 📝 Part 3 ==========
    blocks.append(bh("📝 Part 3"))

    part3 = eval_data.get('part3', [])
    for i, q in enumerate(part3, 1):
        blocks.append(bh(f"Q{i}：{q.get('question', '')}", level=3))
        blocks.append(bp(f"【原文】{q.get('transcript', '')}"))
        blocks.append(bp(f"【得分】Band {q.get('band', 'N/A')}"))

        ana = q.get('analysis', {}) or {}
        sentences = ana.get('sentences', [])

        if sentences:
            sent_lines = []
            for s in sentences:
                sid = s.get('id', 0)
                stext = s.get('text', '')
                diag = s.get('diagnosis', '')
                fix = s.get('fix', '')

                if '✅' in diag:
                    sent_lines.append(f"S{sid}. {stext} → ✅")
                elif fix:
                    sent_lines.append(f"S{sid}. {stext} → {diag} | → {fix}")
                else:
                    sent_lines.append(f"S{sid}. {stext} → {diag}")

            blocks.append(bp("【诊断】" + "｜".join(sent_lines)))

            summary = ana.get('summary', {})
            if summary:
                blocks.append(bp(f"【总结】GRA:{summary.get('grammar','')}｜LR:{summary.get('vocabulary','')}｜FC:{summary.get('logic','')}"))

    # ========== 🎯 总结 ==========
    summary = eval_data.get('summary', {})
    if summary:
        blocks.append(bh("🎯 总结"))
        blocks.append(bp(f"📈 优势：{summary.get('优势', 'N/A')}"))
        blocks.append(bp(f"📉 失分：{summary.get('致命失分点', 'N/A')}"))
        blocks.append(bp(f"🚀 处方：{summary.get('action_plan', 'N/A')}"))

    # ========== 🏆 最终评分 ==========
    blocks.append(bh("🏆 最终评分"))
    blocks.append(bp(f"Overall Band：{data.get('overall_band', 'N/A')}"))
    blocks.append(bp(f"P1均:{scores.get('part1_avg','N/A')} | P2:{scores.get('part2','N/A')} | P3均:{scores.get('part3_avg','N/A')}"))

    # 过滤
    blocks = [b for b in blocks if b is not None]

    print(f"[DEBUG] Total blocks: {len(blocks)}", file=sys.stderr)

    # 计算各部分band
    p1_avg = scores.get('part1_avg', 0)
    p2_band = scores.get('part2', 0)
    p3_avg = scores.get('part3_avg', 0)
    overall = data.get('overall_band', 0)

    # ========== 创建页面（带数据库属性）==========
    # 属性名必须与 create_homework_db.py 中定义的完全一致
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": DB_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": display_name}}]},
            "学生昵称": {"rich_text": [{"text": {"content": data.get('student_nickname', '')}}]},
            "快捷ID": {"rich_text": [{"text": {"content": data.get('topic_short_id', '')}}]},
            "题目类别": {"select": {"name": data.get('topic_category', '未分类')}},
            "综合BandScore": {"number": overall},
            "Part1BandScore": {"number": p1_avg},
            "Part2BandScore": {"number": p2_band},
            "Part3BandScore": {"number": p3_avg},
            "时间戳": {"date": {"start": datetime.now().strftime('%Y-%m-%d')}}
        },
        "children": blocks
    }

    data_bytes = json.dumps(payload, ensure_ascii=False).encode()
    req = urllib.request.Request(url, data=data_bytes, method="POST")
    req.add_header("Authorization", f"Bearer {NOTION_TOKEN}")
    req.add_header("Notion-Version", "2022-06-28")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.load(resp)
            return result.get("id", "")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        print(f"创建作业页面失败: HTTP {e.code} - {err_body[:500]}", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"创建作业页面失败: {e}", file=sys.stderr)
        return ""


# ========== 辅助函数 ==========

def safe_rich_text(text: str) -> list:
    if not text or not str(text).strip():
        return []
    return [{"text": {"content": str(text)[:2000]}}]


def bh(text: str, level: int = 2) -> dict:
    heading_type = f"heading_{level}"
    rich = safe_rich_text(text)
    if not rich:
        return None
    return {"object": "block", "type": heading_type, heading_type: {"rich_text": rich}}


def bp(text: str) -> dict:
    rich = safe_rich_text(text)
    if not rich:
        return None
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": rich}}


def bb(text: str) -> dict:
    rich = safe_rich_text(text)
    if not rich:
        return None
    return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": rich}}


if __name__ == "__main__":
    data = sys.stdin.read().strip()
    try:
        args = json.loads(data)
        page_id = create_homework_v2(args)
        print(json.dumps({"ok": bool(page_id), "page_id": page_id}))
    except json.JSONDecodeError as e:
        print(json.dumps({"ok": False, "page_id": "", "error": f"JSON parse error: {e}"}))
