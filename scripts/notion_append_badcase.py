#!/usr/bin/env python3
"""
追加错题记录到 Notion Bad Case错题本
"""
import sys
import json
import urllib.request
from datetime import datetime

NOTION_TOKEN = "YOUR_NOTION_TOKEN"
DB_ID = "3412e55d-7136-8113-aa98-cfd36af9799c"  # 新建的Bad Case库

def append_badcase(
    student_id: str,
    topic: str,
    student_wrong_answer: str,
    ai_judgment: str,
    teacher_correction: str,
    final_band: float,
    error_types: list = None
) -> str:
    """
    创建Bad Case记录
    所有内容写入正文，properties只保留Name
    """
    # 生成标题
    display_name = f"错题-{student_id[:8] if student_id else 'unknown'}-{topic[:15]}"
    
    # 构建正文blocks
    blocks = []
    
    # 基本信息
    blocks.append({
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": [{"text": {"content": "📋 基本信息"}}]}
    })
    blocks.append({
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": [{"text": {"content": f"学生ID：{student_id}"}}]}
    })
    blocks.append({
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": [{"text": {"content": f"原始题目：{topic}"}}]}
    })
    blocks.append({
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": [{"text": {"content": f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}"}}]}
    })
    
    # 错误类型
    if error_types:
        blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"text": {"content": "🏷️ 错误类型"}}]}
        })
        for et in error_types:
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"text": {"content": et}}]}
            })
    
    # 学生错误答案
    if student_wrong_answer:
        blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"text": {"content": "❌ 学生错误答案"}}]}
        })
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"text": {"content": student_wrong_answer}}]}
        })
    
    # AI原评判
    if ai_judgment:
        blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"text": {"content": "🤖 AI原评判"}}]}
        })
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"text": {"content": ai_judgment}}]}
        })
    
    # 老师正确纠正
    if teacher_correction:
        blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"text": {"content": "✅ 老师正确纠正"}}]}
        })
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"text": {"content": teacher_correction}}]}
        })
    
    # 最终Band
    if final_band:
        blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"text": {"content": "📊 最终Band Score"}}]}
        })
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"text": {"content": f"Band Score：{final_band} / 9.0"}}]}
        })
    
    # 创建页面
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": DB_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": display_name}}]}
        },
        "children": blocks
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {NOTION_TOKEN}")
    req.add_header("Notion-Version", "2022-06-28")
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.load(resp)
            return result.get("id", "")
    except Exception as e:
        print(f"创建Bad Case失败: {e}", file=sys.stderr)
        return ""


if __name__ == "__main__":
    args = json.load(sys.stdin)
    page_id = append_badcase(**args)
    print(json.dumps({"ok": bool(page_id), "page_id": page_id}))
