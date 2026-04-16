#!/usr/bin/env python3
"""创建新的作业反馈库到Notion
1. 先在题库中创建一个页面
2. 用该页面作为父级创建数据库
"""
import json
import urllib.request
import urllib.error

NOTION_TOKEN = "YOUR_NOTION_TOKEN"
QUESTION_BANK_DB = "bba82871-4fe1-4409-9f70-72f6bf27e7b3"  # 题库DB

def create_page_in_db(database_id: str) -> str:
    """在数据库中创建一个页面"""
    url = "https://api.notion.com/v1/pages"

    payload = {
        "parent": {"type": "database_id", "database_id": database_id},
        "properties": {
            "题目": {
                "title": [
                    {"type": "text", "text": {"content": "📚 作业反馈库（父页面）"}}
                ]
            }
        }
    }

    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {NOTION_TOKEN}")
    req.add_header("Notion-Version", "2022-06-28")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.load(resp)
            if result.get("id"):
                print(f"✅ 父级页面创建成功: {result['id']}")
                return result["id"]
            else:
                print(f"❌ 父级页面创建失败: {result}")
                return None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"❌ HTTP错误 {e.code}: {error_body[:500]}")
        return None

def create_homework_db(parent_page_id: str) -> str:
    """在父页面下创建作业反馈库"""
    url = "https://api.notion.com/v1/databases"

    payload = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [
            {"type": "text", "text": {"content": "作业反馈库"}}
        ],
        "properties": {
            "Name": {
                "title": {}
            },
            "学生昵称": {
                "rich_text": {}
            },
            "题目类别": {
                "select": {
                    "options": [
                        {"name": "👤人物类", "color": "blue"},
                        {"name": "📝事件类", "color": "purple"},
                        {"name": "🎁物品类", "color": "orange"},
                        {"name": "🌍地点类", "color": "green"},
                        {"name": "📱媒体类", "color": "red"},
                    ]
                }
            },
            "快捷ID": {
                "rich_text": {}
            },
            "题目编号": {
                "number": {"format": "number"}
            },
            "Part1答案原文": {
                "rich_text": {}
            },
            "Part1BandScore": {
                "number": {"format": "number"}
            },
            "Part2答案原文": {
                "rich_text": {}
            },
            "Part3答案原文": {
                "rich_text": {}
            },
            "Part2BandScore": {
                "number": {"format": "number"}
            },
            "Part3BandScore": {
                "number": {"format": "number"}
            },
            "逐句反馈分析": {
                "rich_text": {}
            },
            "综合BandScore": {
                "number": {"format": "number"}
            },
            "时间戳": {
                "date": {}
            }
        }
    }

    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {NOTION_TOKEN}")
    req.add_header("Notion-Version", "2022-06-28")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.load(resp)
            if result.get("id"):
                print(f"✅ 作业反馈库创建成功！")
                print(f"   Database ID: {result['id']}")
                return result["id"]
            else:
                print(f"❌ 创建失败: {result}")
                return None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"❌ HTTP错误 {e.code}: {error_body[:500]}")
        return None

def update_files(new_db_id: str):
    """更新所有脚本和文档中的DB_ID"""
    import re

    files_to_update = [
        ("scripts/notion_append_homework.py", "DB_ID"),
        ("scripts/evaluate_weekly.py", "HOMEWORK_DB"),
    ]

    for filepath, var_name in files_to_update:
        try:
            with open(filepath, "r") as f:
                content = f.read()

            # 替换 DB_ID
            new_content = re.sub(
                r'(?P<var>' + var_name + r') = "[a-f0-9-]{36}"',
                r'\g<var> = "' + new_db_id + '"',
                content
            )

            with open(filepath, "w") as f:
                f.write(new_content)

            print(f"✅ 已更新 {filepath}")
        except Exception as e:
            print(f"⚠️ 更新 {filepath} 失败: {e}")

    # 更新 SKILL.md
    try:
        with open("SKILL.md", "r") as f:
            content = f.read()

        # 替换旧的DB_ID
        new_content = re.sub(
            r'3412e55d-7136-81ef-afa4-e15492d9da6e',
            new_db_id,
            content
        )

        with open("SKILL.md", "w") as f:
            f.write(new_content)

        print(f"✅ 已更新 SKILL.md")
    except Exception as e:
        print(f"⚠️ 更新 SKILL.md 失败: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("创建作业反馈库")
    print("=" * 50)

    # Step 1: 在题库中创建父级页面
    print("\n[1/2] 在题库中创建父级页面...")
    parent_page_id = create_page_in_db(QUESTION_BANK_DB)

    if not parent_page_id:
        print("\n❌ 无法创建父级页面，请检查题库ID是否正确")
        print(f"当前题库ID: {QUESTION_BANK_DB}")
        exit(1)

    # Step 2: 在父页面下创建数据库
    print("\n[2/2] 创建作业反馈库...")
    db_id = create_homework_db(parent_page_id)

    if not db_id:
        print("\n❌ 无法创建数据库")
        exit(1)

    # Step 3: 更新所有文件中的DB_ID
    print("\n[3/3] 更新脚本和文档中的DB_ID...")
    update_files(db_id)

    print("\n" + "=" * 50)
    print("✅ 全部完成！")
    print("=" * 50)
    print(f"\n📋 新作业反馈库信息：")
    print(f"   Database ID: {db_id}")
    print(f"   父页面ID: {parent_page_id}")
    print(f"\n💡 你可以在Notion中看到这个新库了")
    print(f"   路径：题库 → 📚 作业反馈库（父页面） → 作业反馈库")
