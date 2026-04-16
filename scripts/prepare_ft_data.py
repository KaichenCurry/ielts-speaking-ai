#!/usr/bin/env python3
"""
微调数据准备脚本 - 从错题本生成微调数据集

用途：
  1. 将老师的/纠正记录转换为微调训练数据
  2. 生成JSONL格式的训练集/验证集
  3. 数据质量检查

微调样本格式：
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "学生回答：..."},
    {"role": "assistant", "content": "【逐句反馈】..."}
  ]
}

触发条件：
  - 错题本积累 ≥ 100条
  - 评估显示系统性偏差
"""
import sys
import json
import urllib.request
from datetime import datetime
from collections import Counter

# ============ 配置 ============
NOTION_TOKEN = "YOUR_NOTION_TOKEN"
BADCASE_DB = "3412e55d-7136-8113-aa98-cfd36af9799c"
# ==============================

# 微调System Prompt
FT_SYSTEM_PROMPT = """你是一个专业的雅思口语个性化反馈老师。

核心任务：根据学生实际说的每一句话，从5个维度给出个性化反馈：
- 语法：句子结构、主谓一致、从句使用、介词搭配
- 词汇：用词地道性、Chinglish、高分词汇替换
- 时态：过去时、现在时、完成时准确性
- 逻辑：因果关系、转折层次、是否跑题
- 思路：举例具体性、观点深度、论证力度

反馈原则：
1. 逐句分析，不漏一句
2. 针对学生实际说的内容，不对照任何标准答案
3. 每句话给出：✅做好的地方、❌需改进的地方、💡优化建议
4. 最终给出Band Score和1-2条最需突破的改进建议

输出格式：Markdown表格，包含逐句剖析、问题汇总、Band Score、改进建议"""

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

def get_all_badcases(limit: int = 500) -> list:
    """获取所有已纠正的错题本记录"""
    payload = {
        "filter": {
            "property": "老师已校对",
            "checkbox": {"equals": True}
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

def create_ft_sample(badcase: dict) -> dict:
    """
    将一条错题本记录转换为微调样本

    训练思路：
    - 输入：学生回答 + 老师纠正的反馈（作为"标准答案"）
    - 输出：应该生成的逐句反馈

    注意：我们用老师的纠正作为"正确答案"来训练模型
    """
    # 构建user消息（学生回答）
    user_content = f"""学生回答：
{badcase['学生错误答案']}

题目：{badcase['原始题目']}

请对学生的回答进行逐句个性化反馈。"""

    # 构建assistant消息（老师纠正后的正确反馈）
    # 注意：这里实际上AI不知道正确的反馈是什么
    # 更好的方式是让老师直接标注"应该怎么反馈"
    # 当前方案：使用AI评判 + 老师纠正的组合作为训练目标
    assistant_content = f"""【逐句反馈】

原始AI评判：
{badcase['AI原评判']}

老师纠正：
{badcase['老师正确纠正']}

最终Band Score：{badcase['最终BandScore']}"""

    return {
        "messages": [
            {"role": "system", "content": FT_SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": assistant_content}
        ]
    }

def validate_sample(sample: dict) -> tuple:
    """
    验证微调样本质量
    返回：(is_valid, error_message)
    """
    messages = sample.get("messages", [])

    # 检查必填字段
    if len(messages) != 3:
        return False, f"消息数量应为3，实际{len(messages)}"

    # 检查角色
    roles = [m.get("role") for m in messages]
    if roles != ["system", "user", "assistant"]:
        return False, f"角色顺序错误: {roles}"

    # 检查内容长度
    user_content = messages[1].get("content", "")
    assistant_content = messages[2].get("content", "")

    if len(user_content) < 10:
        return False, "学生回答过短"

    if len(assistant_content) < 20:
        return False, "反馈内容过短"

    return True, ""

def analyze_dataset(samples: list) -> dict:
    """分析数据集质量"""
    stats = {
        "total": len(samples),
        "valid": 0,
        "invalid": 0,
        "errors": Counter(),
        "band_distribution": Counter(),
        "error_type_distribution": Counter(),
    }

    for sample in samples:
        is_valid, error = validate_sample(sample)
        if is_valid:
            stats["valid"] += 1
        else:
            stats["invalid"] += 1
            stats["errors"][error] += 1

        # Band分布
        try:
            band = sample["messages"][2]["content"].split("最终Band Score：")[1].split("\n")[0]
            stats["band_distribution"][band] += 1
        except (IndexError, KeyError):
            pass

    return stats

def split_dataset(samples: list, train_ratio: float = 0.8) -> tuple:
    """分割训练集/验证集"""
    import random
    random.seed(42)  # 固定种子，保证可复现

    # 打乱
    shuffled = samples.copy()
    random.shuffle(shuffled)

    # 分割
    split_idx = int(len(shuffled) * train_ratio)
    train_set = shuffled[:split_idx]
    val_set = shuffled[split_idx:]

    return train_set, val_set

def prepare_ft_data(min_samples: int = 100, output_dir: str = ".") -> dict:
    """
    主函数：准备微调数据集

    Args:
        min_samples: 最低样本量要求
        output_dir: 输出目录

    Returns:
        dict: 准备结果
    """
    print("=" * 60)
    print("微调数据准备")
    print("=" * 60)

    # 1. 检查数据量
    print("\n📊 检查错题本数据量...")
    badcases = get_all_badcases()
    print(f"  • 错题本总数：{len(badcases)}条")
    print(f"  • 要求最低：{min_samples}条")

    if len(badcases) < min_samples:
        print(f"\n⚠️ 数据量不足！当前{len(badcases)}条，需要{min_samples}条")
        print("提示：继续积累更多/纠正数据，或降低min_samples要求")
        return {
            "success": False,
            "current_count": len(badcases),
            "required_count": min_samples,
            "message": f"数据量不足，需要{min_samples - len(badcases)}条"
        }

    print(f"\n✅ 数据量满足要求！")

    # 2. 转换为微调样本
    print("\n🔄 转换为微调样本...")
    samples = []
    invalid_samples = []

    for bc in badcases:
        sample = create_ft_sample(bc)
        is_valid, error = validate_sample(sample)

        if is_valid:
            samples.append(sample)
        else:
            invalid_samples.append((bc, error))

    print(f"  • 有效样本：{len(samples)}条")
    print(f"  • 无效样本：{len(invalid_samples)}条")

    if invalid_samples:
        print("\n  无效样本原因：")
        error_counts = Counter([e for _, e in invalid_samples])
        for error, count in error_counts.most_common(5):
            print(f"    • {error}: {count}条")

    # 3. 分析数据集
    print("\n📈 数据集分析...")
    stats = analyze_dataset(samples)
    print(f"  • 总样本：{stats['total']}条")
    print(f"  • 有效样本：{stats['valid']}条")

    # 4. 分割数据集
    print("\n✂️ 分割训练集/验证集（80%/20%）...")
    train_set, val_set = split_dataset(samples, train_ratio=0.8)
    print(f"  • 训练集：{len(train_set)}条")
    print(f"  • 验证集：{len(val_set)}条")

    # 5. 写入文件
    print(f"\n💾 写入文件到 {output_dir}...")
    train_file = f"{output_dir}/ft_train.jsonl"
    val_file = f"{output_dir}/ft_val.jsonl"

    with open(train_file, "w", encoding="utf-8") as f:
        for sample in train_set:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")

    with open(val_file, "w", encoding="utf-8") as f:
        for sample in val_set:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")

    print(f"  ✅ 训练集：{train_file}")
    print(f"  ✅ 验证集：{val_file}")

    # 6. 总结
    print("\n" + "=" * 60)
    print("✅ 微调数据准备完成！")
    print("=" * 60)
    print(f"\n📋 下一步：")
    print(f"  1. 检查 {train_file} 和 {val_file} 的内容")
    print(f"  2. 使用OpenAI微调命令提交任务：")
    print(f"     openai api fine_tunes.create -t {train_file} -v {val_file}")
    print(f"  3. 或使用其他微调平台（如Claude、LlamaFactory等）")

    return {
        "success": True,
        "total_samples": len(samples),
        "train_samples": len(train_set),
        "val_samples": len(val_set),
        "train_file": train_file,
        "val_file": val_file,
        "stats": stats
    }

if __name__ == "__main__":
    import os

    # 支持命令行参数
    min_samples = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    result = prepare_ft_data(min_samples=min_samples, output_dir=output_dir)

    if not result["success"]:
        print(f"\n❌ 准备失败：{result['message']}")
        sys.exit(1)
