#!/usr/bin/env python3
"""
逐个修复题库中的Test
"""
import urllib.request
import json
import time

NOTION_TOKEN = "YOUR_NOTION_TOKEN"
DB_ID = "bba82871-4fe1-4409-9f70-72f6bf27e7b3"
MAX_PART1 = 5
MAX_PART3 = 5

def api(url, method="GET", data=None):
    req = urllib.request.Request(url, data=data.encode() if data else None, method=method)
    req.add_header("Authorization", f"Bearer {NOTION_TOKEN}")
    req.add_header("Notion-Version", "2022-06-28")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.load(resp)
    except Exception as e:
        print(f"API Error: {e}")
        return None

def get_all_pages():
    """获取所有页面"""
    pages = []
    cursor = None
    while True:
        payload = {"page_size": 100}
        if cursor:
            payload["start_cursor"] = cursor
        result = api(f"https://api.notion.com/v1/databases/{DB_ID}/query", method="POST", data=json.dumps(payload))
        if not result:
            break
        pages.extend(result.get("results", []))
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")
    return pages

def get_blocks(page_id):
    result = api(f"https://api.notion.com/v1/blocks/{page_id}/children")
    return result.get("results", []) if result else []

def delete_block(block_id):
    api(f"https://api.notion.com/v1/blocks/{block_id}", method="DELETE")

def append_children(page_id, blocks):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    # 分批，每批最多100个
    for i in range(0, len(blocks), 100):
        batch = blocks[i:i+100]
        api(url, method="PATCH", data=json.dumps({"children": batch}))
        time.sleep(0.3)

def count_questions(blocks):
    p1 = p3 = 0
    section = None
    for b in blocks:
        btype = b.get("type")
        rich = b.get(btype, {}).get("rich_text", [])
        text = "".join([t.get("text", {}).get("content", "") for t in rich])
        if btype in ["heading_1", "heading_2"]:
            if text == "Part 1": section = "P1"
            elif text == "Part 3": section = "P3"
            elif text == "Part 2": section = "P2"
        elif btype == "bulleted_list_item" and section == "P1":
            p1 += 1
        elif btype == "numbered_list_item" and section == "P3":
            p3 += 1
    return p1, p3

def rebuild_blocks(blocks):
    """重建blocks"""
    new_blocks = []
    section = None
    p1 = p3 = 0
    
    for b in blocks:
        btype = b.get("type")
        rich = b.get(btype, {}).get("rich_text", [])
        text = "".join([t.get("text", {}).get("content", "") for t in rich])
        
        # 章节检测
        if btype in ["heading_1", "heading_2"]:
            if text == "Part 1":
                section = "P1"
                p1 = 0
                new_blocks.append(b)
            elif text == "Part 3":
                section = "P3"
                p3 = 0
                new_blocks.append(b)
            elif text == "Part 2":
                section = "P2"
                new_blocks.append(b)
            else:
                section = None
        
        elif btype == "heading_3" and section == "P1" and p1 < MAX_PART1:
            new_blocks.append(b)
        
        elif btype == "bulleted_list_item":
            if section == "P1" and p1 < MAX_PART1:
                new_blocks.append(b)
                p1 += 1
            elif section == "P2":
                new_blocks.append(b)
        
        elif btype == "numbered_list_item" and section == "P3":
            if p3 < MAX_PART3:
                new_text = f"{p3 + 1}. {text.split('. ', 1)[1] if '. ' in text else text}"
                new_blocks.append({"object": "block", "type": btype, btype: {"rich_text": [{"type": "text", "text": {"content": new_text}}]}})
                p3 += 1
        
        elif btype == "paragraph" and section in [None, "P2"]:
            new_blocks.append(b)
        
        elif section in [None, "P2"]:
            new_blocks.append(b)
    
    return new_blocks

def fix_page(page_id, num):
    """修复单个页面"""
    blocks = get_blocks(page_id)
    orig_p1, orig_p3 = count_questions(blocks)
    
    if orig_p1 <= MAX_PART1 and orig_p3 <= MAX_PART3:
        return False
    
    print(f"  Test {num:02d}: P1={orig_p1}, P3={orig_p3} → ", end="", flush=True)
    
    # 重建blocks
    new_blocks = rebuild_blocks(blocks)
    
    # 删除旧blocks
    for b in blocks:
        delete_block(b.get("id"))
        time.sleep(0.05)
    
    # 添加新blocks
    append_children(page_id, new_blocks)
    
    new_p1, new_p3 = count_questions(new_blocks)
    print(f"P1={new_p1}, P3={new_p3}")
    return True

def main():
    print("=" * 50)
    print("修复题库：Part1/Part3最多5题")
    print("=" * 50)
    
    print("\n获取页面列表...")
    pages = get_all_pages()
    print(f"共 {len(pages)} 个页面")
    
    # 找出需要修复的
    to_fix = []
    for page in pages:
        props = page.get("properties", {})
        num = props.get("编号", {}).get("number", 0)
        page_id = page.get("id")
        blocks = get_blocks(page_id)
        p1, p3 = count_questions(blocks)
        if p1 > MAX_PART1 or p3 > MAX_PART3:
            to_fix.append({"num": num, "page_id": page_id, "p1": p1, "p3": p3})
    
    print(f"需要修改: {len(to_fix)} 个")
    print()
    
    # 逐个修复
    fixed = 0
    for item in to_fix:
        if fix_page(item["page_id"], item["num"]):
            fixed += 1
        time.sleep(0.5)
    
    print(f"\n完成！修改了 {fixed}/{len(to_fix)} 个Test")

if __name__ == "__main__":
    main()
