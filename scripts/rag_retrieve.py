#!/usr/bin/env python3
"""
RAG检索脚本 - 从Notion获取相关上下文
用于评分时注入历史错题/同类回答作为参考

用法：
  python rag_retrieve.py "社交媒体" --type all --limit 3
  python rag_retrieve.py "社交媒体" --type badcase --limit 5
  python rag_retrieve.py "社交媒体" --type homework --limit 3
"""
import sys
import json
import urllib.request
import argparse
from datetime import datetime, timedelta

# ============ 配置 ============
NOTION_TOKEN = "YOUR_NOTION_TOKEN"
BADCASE_DB = "3412e55d-7136-8113-aa98-cfd36af9799c"
HOMEWORK_DB = "3412e55d-7136-8179-9ac8-ee60a420ac21"
# ==============================

def get_text(prop):
    """从任意prop提取纯文本"""
    if not prop:
        return ""
    t = prop.get("type", "")
    if t == "title":
        return "".join([x.get("plain_text", "") for x in prop.get("title", [])])
    if t == "rich_text":
        return "".join([x.get("plain_text", "") for x in prop.get("rich_text", [])])
    if t == "select":
        return (prop.get("select") or {}).get("name", "")
    if t == "multi_select":
        return ", ".join([x.get("name", "") for x in prop.get("multi_select", [])])
    if t == "checkbox":
        return "是" if prop.get("checkbox") else "否"
    return ""

def notion_query(database_id: str, payload: dict) -> list:
    """查询Notion数据库"""
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {NOTION_TOKEN}")
    req.add_header("Notion-Version", "2022-06-28")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.load(resp).get("results", [])
    except Exception as e:
        print(f"Notion查询失败: {e}", file=sys.stderr)
        return []

def retrieve_badcases(topic: str, limit: int = 5) -> list:
    """从错题本检索同类话题的错误模式"""
    payload = {
        "filter": {
            "property": "原始题目",
            "rich_text": {"contains": topic}
        },
        "page_size": limit,
        "sorts": [{"timestamp": "created_time", "direction": "descending"}]
    }
    results = notion_query(BADCASE_DB, payload)

    badcases = []
    for page in results:
        props = page.get("properties", {})
        badcases.append({
            "学生ID": get_text(props.get("学生ID")),
            "原始题目": get_text(props.get("原始题目")),
            "学生错误答案": get_text(props.get("学生错误答案")),
            "AI原评判": get_text(props.get("AI原评判")),
            "老师正确纠正": get_text(props.get("老师正确纠正")),
            "错误类型": get_text(props.get("错误类型")),
            "最终BandScore": props.get("最终BandScore", {}).get("number") or 0,
            "时间戳": get_text(props.get("时间戳")),
        })
    return badcases

def retrieve_homeworks(topic: str, limit: int = 3) -> list:
    """从作业反馈库检索同类话题的学生回答"""
    payload = {
        "filter": {
            "property": "快捷ID",
            "rich_text": {"contains": topic}
        },
        "page_size": limit,
        "sorts": [{"timestamp": "created_time", "direction": "descending"}]
    }
    results = notion_query(HOMEWORK_DB, payload)

    homeworks = []
    for page in results:
        props = page.get("properties", {})
        homeworks.append({
            "学生昵称": get_text(props.get("学生昵称")),
            "快捷ID": get_text(props.get("快捷ID")),
            "题目类别": get_text(props.get("题目类别")),
            "Part2答案原文": get_text(props.get("Part2答案原文")),
            "Part3答案原文": get_text(props.get("Part3答案原文")),
            "逐句反馈分析": get_text(props.get("逐句反馈分析")),
            "综合BandScore": props.get("综合BandScore", {}).get("number") or 0,
            "时间戳": get_text(props.get("时间戳")),
        })
    return homeworks

def format_rag_context(topic: str, badcases: list, homeworks: list) -> str:
    """格式化RAG上下文，用于注入Prompt"""
    context_parts = []

    if badcases:
        context_parts.append("【同类话题历史错题】")
        for i, bc in enumerate(badcases, 1):
            context_parts.append(f"\n--- 错题{i} ---")
            context_parts.append(f"题目：{bc['原始题目']}")
            context_parts.append(f"错误类型：{bc['错误类型']}")
            context_parts.append(f"学生答案：{bc['学生错误答案'][:200]}...")
            context_parts.append(f"老师纠正：{bc['老师正确纠正'][:100]}...")

    if homeworks:
        context_parts.append("\n\n【同类话题学生回答参考】")
        for i, hw in enumerate(homeworks, 1):
            context_parts.append(f"\n--- 回答{i} (Band {hw['综合BandScore']}) ---")
            context_parts.append(f"题目：{hw['快捷ID']}")
            if hw['Part2答案原文']:
                context_parts.append(f"Part2回答：{hw['Part2答案原文'][:200]}...")
            if hw['逐句反馈分析']:
                context_parts.append(f"反馈要点：{hw['逐句反馈分析'][:150]}...")

    return "".join(context_parts) if context_parts else ""

def rag_retrieve(topic: str, retrieval_type: str = "all", limit: int = 3) -> dict:
    """
    主检索函数

    Args:
        topic: 话题关键词
        retrieval_type: all / badcase / homework
        limit: 检索数量

    Returns:
        dict: {
            "topic": str,
            "badcases": list,
            "homeworks": list,
            "context": str  # 格式化后的上下文
        }
    """
    result = {
        "topic": topic,
        "retrieval_type": retrieval_type,
        "limit": limit,
        "badcases": [],
        "homeworks": [],
        "context": ""
    }

    if retrieval_type in ("all", "badcase"):
        result["badcases"] = retrieve_badcases(topic, limit)

    if retrieval_type in ("all", "homework"):
        result["homeworks"] = retrieve_homeworks(topic, limit)

    result["context"] = format_rag_context(topic, result["badcases"], result["homeworks"])

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RAG检索脚本")
    parser.add_argument("topic", help="话题关键词，如'社交媒体'")
    parser.add_argument("--type", choices=["all", "badcase", "homework"], default="all", help="检索类型")
    parser.add_argument("--limit", type=int, default=3, help="检索数量")
    args = parser.parse_args()

    result = rag_retrieve(args.topic, args.type, args.limit)

    # 输出格式化上下文（供AI使用）
    if result["context"]:
        print("=" * 50)
        print(f"RAG上下文（话题：{args.topic}）")
        print("=" * 50)
        print(result["context"])
    else:
        print(f"未找到与「{args.topic}」相关的历史数据")

    # 完整JSON输出（供程序使用）
    print("\n--- RAW DATA ---")
    print(json.dumps(result, ensure_ascii=False, indent=2))
