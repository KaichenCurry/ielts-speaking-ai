#!/usr/bin/env python3
"""
雅思口语题库自动扩充脚本
- 每周三、周六自动运行
- 从可靠来源抓取新题 → AI生成完整内容 → 入库到Notion题库

【最新模考题库2026 格式】
- 编号: number (自动递增)
- 题目: title (如"社交媒体趣事 | Test 67")
- 内容在页面正文中：
  - Part 1: heading_2 + heading_3(topic) + bulleted_list_item(questions, 最多5题/topic)
  - Part 2: heading_1 + paragraph(topic) + bulleted_list_item(should_say points)
  - Part 3: heading_2 + numbered_list_item(questions, 最多5题)
"""
import sys
import json
import urllib.request
import urllib.error
import re
from datetime import datetime

# ============ 配置 ============
NOTION_TOKEN = "YOUR_NOTION_TOKEN"
QUESTION_BANK_DB = "bba82871-4fe1-4409-9f70-72f6bf27e7b3"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
OPENAI_BASE_URL = "https://api.openai.com/v1"
MODEL = "gpt-4o-mini"
FETCH_LIMIT = 5  # 每次抓取新题数量
# ==============================

CATEGORIES = ["人物类", "事件类", "物品类", "地点类"]
DIFFICULTIES = ["基础", "中等", "进阶"]

# ============ Notion API ============
def notion_query(sql: dict) -> dict:
    url = f"https://api.notion.com/v1/databases/{QUESTION_BANK_DB}/query"
    data = json.dumps(sql).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {NOTION_TOKEN}")
    req.add_header("Notion-Version", "2022-06-28")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode()[:200]}", file=sys.stderr)
        raise

def notion_create_page(properties: dict) -> str:
    """在题库中创建新页面"""
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": QUESTION_BANK_DB},
        "properties": properties
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
    except urllib.error.HTTPError as e:
        print(f"创建页面失败: {e.read().decode()[:200]}", file=sys.stderr)
        return ""

def notion_append_blocks(page_id: str, blocks: list):
    """向页面追加内容blocks"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    payload = {"children": blocks}
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method="PATCH")
    req.add_header("Authorization", f"Bearer {NOTION_TOKEN}")
    req.add_header("Notion-Version", "2022-06-28")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"追加blocks失败: {e.read().decode()[:200]}", file=sys.stderr)
        return None

def get_next_number() -> int:
    """获取下一个编号"""
    result = notion_query({"page_size": 100})
    max_num = 0
    for page in result.get("results", []):
        num = page.get("properties", {}).get("编号", {}).get("number") or 0
        if num > max_num:
            max_num = num
    return max_num + 1

# ============ AI 生成 ============
def call_ai(prompt: str) -> str:
    """调用 AI 生成内容"""
    url = f"{OPENAI_BASE_URL}/chat/completions"
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
        print(f"  AI生成失败: {e}")
        return ""

def generate_topic_content(topic_en: str) -> dict:
    """
    用 AI 生成完整题目内容
    Part1: 1-3个topics，**总题数不超过5题**
    Part3: 最多5题
    """
    prompt = f"""为以下雅思口语题目，生成符合【最新模考题库2026】格式的完整题目信息。

英文题目：{topic_en}

请生成以下内容的JSON：
{{
    "category": "类型（人物类/事件类/物品类/地点类）",
    "difficulty": "难度（基础/中等/进阶）",
    "part1_topics": [
        {{
            "topic": "Topic名称（英文）",
            "questions": ["问题1", "问题2"]  // 1-3个topics，但**总题数不超过5题**
        }},
        // 可选多个topics，但总题数要控制在5题以内
    ],
    "part2_topic": "Part2话题描述（英文，详细）",
    "part2_points": ["should say point 1", "point 2", "point 3"],  // 3-4个
    "part3_questions": ["追问1", "追问2", "追问3"]  // **最多5题**
}}

要求：
- Part1: **总题数不超过5题**（不管有几个topics）
- Part3: **最多5题**
- Part2: 详细描述，包含when/what/why等问题提示
- 只输出JSON，不要其他内容"""

    result = call_ai(prompt)
    try:
        json_match = re.search(r'\{[\s\S]*\}', result)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        print(f"  JSON解析失败: {e}")

    return None

def build_page_blocks(content: dict) -> list:
    """构建页面内容blocks"""
    blocks = []
    
    # Part 1 - 总题数不超过5题
    blocks.append({
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": [{"text": {"content": "Part 1"}}]}
    })
    
    total_part1 = 0
    max_part1 = 5  # 总题数限制5题
    
    for topic_data in content.get("part1_topics", []):
        topic_name = topic_data.get("topic", "General")
        questions = topic_data.get("questions", [])
        
        # 计算该topic还能放几题
        remaining = max_part1 - total_part1
        if remaining <= 0:
            break
        questions = questions[:remaining]
        
        if questions:
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {"rich_text": [{"text": {"content": f"Topic: {topic_name}"}}]}
            })
            
            for q in questions:
                blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {"rich_text": [{"text": {"content": q}}]}
                })
                total_part1 += 1
    
    # Part 2
    blocks.append({
        "object": "block",
        "type": "heading_1",
        "heading_1": {"rich_text": [{"text": {"content": "Part 2"}}]}
    })
    blocks.append({
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"text": {"content": content.get("part2_topic", "")}}]}
    })
    blocks.append({
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"text": {"content": "You should say:"}}]}
    })
    for point in content.get("part2_points", []):
        blocks.append({
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"text": {"content": point}}]}
        })
    
    # Part 3 - 最多5题
    blocks.append({
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": [{"text": {"content": "Part 3"}}]}
    })
    for i, q in enumerate(content.get("part3_questions", [])[:5], 1):  # 强制最多5题
        blocks.append({
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {"rich_text": [{"text": {"content": f"{i}. {q}"}}]}
        })
    
    return blocks

def create_topic(topic_en: str, short_id: str = ""):
    """创建完整题目"""
    print(f"\n处理题目: {topic_en}")
    
    # 生成内容
    content = generate_topic_content(topic_en)
    if not content:
        print(f"  ❌ AI生成失败")
        return False
    
    # 获取下一个编号
    next_num = get_next_number()
    display_title = f"{short_id} | Test {next_num}" if short_id else f"Test {next_num}"
    
    # 创建页面
    properties = {
        "题目": {"title": [{"text": {"content": display_title}}]},
        "编号": {"number": next_num},
        "类型": {"multi_select": [{"name": content.get("category", "事件类")}]},
        "难度": {"select": {"name": content.get("difficulty", "中等")}},
        "练习状态": {"select": {"name": "新增待练习"}}
    }
    
    page_id = notion_create_page(properties)
    if not page_id:
        print(f"  ❌ 页面创建失败")
        return False
    
    # 追加内容到页面正文
    blocks = build_page_blocks(content)
    notion_append_blocks(page_id, blocks)
    
    print(f"  ✅ 创建成功: {display_title}")
    return True

# ============ 主程序 ============
def main():
    print("=" * 60)
    print("📚 雅思口语题库自动扩充")
    print("=" * 60)
    
    # 从网站获取新题目
    topics = fetch_new_topics()
    
    if not topics:
        print("❌ 没有获取到新题目")
        return
    
    print(f"\n获取到 {len(topics)} 个新题目")
    
    success = 0
    for topic in topics:
        if create_topic(topic):
            success += 1
    
    print(f"\n完成！成功创建 {success}/{len(topics)} 个题目")

def fetch_new_topics() -> list:
    """
    从可靠来源获取新题目
    返回英文话题列表
    """
    # 方法：从ieltsliz.com抓取
    topics = []
    
    try:
        url = "https://ieltsliz.com/cue-cards/"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
        # 提取Part 2题目（以Describe/Talk about开头）
        pattern = r'(Describe|Talk about|Explain|Tell me about)[^<]{10,100}'
        matches = re.findall(pattern, html, re.IGNORECASE)
        
        for m in matches[:FETCH_LIMIT]:
            topic = m.strip()
            if len(topic) > 20:  # 过滤太短的
                topics.append(topic)
    except Exception as e:
        print(f"抓取失败: {e}")
    
    # 如果抓取失败，使用备用题目
    if not topics:
        backup_topics = [
            "Describe a famous person you would like to meet",
            "Describe a place you would like to visit",
            "Describe a memorable trip you took",
            "Describe a skill you would like to learn",
            "Describe a book that influenced you deeply"
        ]
        topics = backup_topics[:FETCH_LIMIT]
    
    return topics

if __name__ == "__main__":
    main()
