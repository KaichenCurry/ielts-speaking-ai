#!/usr/bin/env python3
"""
重建错题本数据库的字段结构
"""
import urllib.request
import json

NOTION_TOKEN = "YOUR_NOTION_TOKEN"
DB_ID = "3412e55d-7136-8113-aa98-cfd36af9799c"

# 新的schema
NEW_SCHEMA = {
    "学生ID": {"rich_text": {}},
    "原始题目": {"rich_text": {}},
    "学生错误答案": {"rich_text": {}},
    "AI原评判": {"rich_text": {}},
    "老师正确纠正": {"rich_text": {}},
    "最终BandScore": {"number": {"format": "number"}},
    "老师已校对": {"checkbox": {}},
    "时间戳": {"date": {}}
}

url = f"https://api.notion.com/v1/databases/{DB_ID}"
payload = {"properties": NEW_SCHEMA}
data = json.dumps(payload).encode()
req = urllib.request.Request(url, data=data, method="PATCH")
req.add_header("Authorization", f"Bearer {NOTION_TOKEN}")
req.add_header("Notion-Version", "2022-06-28")
req.add_header("Content-Type", "application/json")

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.load(resp)
        print("✅ 错题本schema更新成功!")
        print(f"新增字段: {list(NEW_SCHEMA.keys())}")
except Exception as e:
    print(f"❌ 更新失败: {e}")
