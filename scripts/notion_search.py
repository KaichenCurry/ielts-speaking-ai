#!/usr/bin/env python3
"""
Notion题库搜索 - 适配新版数据库结构
DB: bba82871-4fe1-4409-9f70-72f6bf27e7b3 (雅思最新口语题库2026)
"""
import urllib.request
import json
import re
import sys

NOTION_TOKEN = "YOUR_NOTION_TOKEN"
NEW_DB = "bba82871-4fe1-4409-9f70-72f6bf27e7b3"

def api(url, method="GET", data=None):
    if data is not None and isinstance(data, str):
        data = data.encode()
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {NOTION_TOKEN}")
    req.add_header("Notion-Version", "2022-06-28")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.load(resp)
    except Exception as e:
        return {"error": str(e)}

def get_title_text(rich_text_list):
    """从rich_text列表提取纯文本"""
    if not rich_text_list:
        return ""
    return "".join([t.get("plain_text", "") for t in rich_text_list])

def get_select_name(select_obj):
    """从select对象提取name"""
    if not select_obj:
        return ""
    if isinstance(select_obj, dict):
        return select_obj.get("name", "")
    return ""

def get_page_blocks(page_id):
    """获取页面所有blocks"""
    blocks = []
    cursor = None
    while True:
        url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        if cursor:
            url += f"?start_cursor={cursor}"
        result = api(url)
        if result is None or "results" not in result:
            break
        blocks.extend(result.get("results", []))
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")
    return blocks

def extract_content_from_blocks(blocks):
    """从blocks中提取Part1/2/3内容"""
    content = {
        "Part 1": [],
        "Part 2": {"topic": "", "should_say": []},
        "Part 3": []
    }
    
    current_section = None
    in_part2_should_say = False
    
    for block in blocks:
        btype = block.get("type")
        rich = block.get(btype, {}).get("rich_text", [])
        text = get_title_text(rich)
        
        if btype == "heading_2":
            if "Part 1" in text:
                current_section = "Part 1"
                in_part2_should_say = False
            elif "Part 2" in text:
                current_section = "Part 2"
                in_part2_should_say = False
            elif "Part 3" in text:
                current_section = "Part 3"
                in_part2_should_say = False
            else:
                current_section = None
        elif btype == "bulleted_list_item":
            if current_section == "Part 1":
                content["Part 1"].append(text)
            elif current_section == "Part 2":
                if "You should say" in text or "should say" in text.lower():
                    in_part2_should_say = True
                elif in_part2_should_say:
                    content["Part 2"]["should_say"].append(text)
        elif btype == "numbered_list_item":
            if current_section == "Part 3":
                content["Part 3"].append(text)
        elif btype == "paragraph":
            if current_section == "Part 2" and text:
                if not content["Part 2"]["topic"]:
                    content["Part 2"]["topic"] = text
                elif "You should say" in text or "should say" in text.lower():
                    in_part2_should_say = True
    
    return content

def search_test(keyword: str) -> dict:
    """
    搜索最新模考题库
    keyword格式: "Test 01" / "Test 1" / "社交媒体" 等
    返回: 完整题目内容
    """
    # 解析Test编号
    test_num = None
    clean_kw = keyword.strip()
    
    # 匹配 Test XX 或 Test X 格式
    m = re.match(r'[Tt]est\s*(\d+)', clean_kw)
    if m:
        test_num = int(m.group(1))
    
    results = None
    
    if test_num is not None:
        # 按标题精确查找 (格式: "Test XX · 话题")
        # 使用starts_with匹配 "Test XX ·"
        payload = {
            "filter": {
                "property": "话题",
                "title": {"starts_with": f"Test {test_num:02d}"}
            },
            "page_size": 5
        }
        url = f"https://api.notion.com/v1/databases/{NEW_DB}/query"
        data = json.dumps(payload)
        result = api(url, method="POST", data=data)
        results = result.get("results", []) if result else []
    
    if not results:
        # 按话题名模糊搜索
        payload = {
            "filter": {
                "property": "话题",
                "title": {"contains": clean_kw}
            },
            "page_size": 5
        }
        url = f"https://api.notion.com/v1/databases/{NEW_DB}/query"
        data = json.dumps(payload)
        result = api(url, method="POST", data=data)
        results = result.get("results", []) if result else []
    
    if not results:
        return {"found": False, "keyword": keyword}
    
    page = results[0]
    props = page.get("properties", {})
    page_id = page.get("id", "")
    
    # 解析标题获取Test编号
    title_rich = props.get("话题", {}).get("title", [])
    title_text = get_title_text(title_rich)
    
    # 提取Test编号
    test_number = None
    m = re.match(r'Test\s*(\d+)', title_text)
    if m:
        test_number = int(m.group(1))
    
    # 获取页面正文内容
    blocks = get_page_blocks(page_id)
    content = extract_content_from_blocks(blocks)
    
    # 获取元数据
    category = get_select_name(props.get("类型", {}).get("select"))
    difficulty = get_select_name(props.get("难度", {}).get("select"))
    
    # 提取中文话题名（标题中·后面部分）
    topic_cn = ""
    if "·" in title_text:
        topic_cn = title_text.split("·", 1)[1].strip()
    else:
        topic_cn = title_text
    
    return {
        "found": True,
        "test_number": test_number,
        "title": title_text,
        "topic_cn": topic_cn,
        "Part 1": content["Part 1"],
        "Part 2 topic": content["Part 2"]["topic"],
        "Part 2 should_say": content["Part 2"]["should_say"],
        "Part 3": content["Part 3"],
        "category": category,
        "difficulty": difficulty,
        "page_id": page_id,
    }

def list_all_tests() -> list:
    """列出所有Test"""
    url = f"https://api.notion.com/v1/databases/{NEW_DB}/query"
    result = api(url, method="POST", data=json.dumps({"page_size": 100}))
    pages = result.get("results", []) if result else []
    
    tests = []
    for page in pages:
        props = page.get("properties", {})
        title_rich = props.get("话题", {}).get("title", [])
        title_text = get_title_text(title_rich)
        
        m = re.match(r'Test\s*(\d+)', title_text)
        test_num = int(m.group(1)) if m else None
        
        if test_num:
            tests.append({
                "test_number": test_num,
                "title": title_text
            })
    
    tests.sort(key=lambda x: x["test_number"])
    return tests

if __name__ == "__main__":
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
        result = search_test(keyword)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 列出所有Test
        tests = list_all_tests()
        print(f"总共有 {len(tests)} 个Test:")
        for t in tests:
            print(f"  Test {t['test_number']:02d}")
