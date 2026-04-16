#!/usr/bin/env python3
"""
每周评估脚本 - 计算AI评分准确率

触发方式：
  1. 定时任务（每周五18:00自动运行）
  2. 手动执行：python evaluate_weekly.py

评估指标：
  - Band误差：AI Band vs 老师纠正后Band
  - 各维度准确率：语法/词汇/时态/逻辑/思路
  - 错题命中率

输出：
  - 控制台输出评估报告
  - 结果写入Notion评估记录库（可选）
"""
import sys
import json
import urllib.request
from datetime import datetime, timedelta
from collections import defaultdict

# ============ 配置 ============
NOTION_TOKEN = "YOUR_NOTION_TOKEN"
BADCASE_DB = "3412e55d-7136-8113-aa98-cfd36af9799c"
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

def get_recent_badcases(days: int = 7, limit: int = 50) -> list:
    """获取最近N天的错题本记录"""
    # 计算日期范围
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    payload = {
        "filter": {
            "and": [
                {"property": "老师已校对", "checkbox": {"equals": True}},
                {"property": "时间戳", "date": {"on_or_after": start_date.strftime("%Y-%m-%d")}}
            ]
        },
        "page_size": limit,
        "sorts": [{"timestamp": "created_time", "direction": "descending"}]
    }

    results = notion_query(BADCASE_DB, payload)

    badcases = []
    for page in results:
        props = page.get("properties", {})
        ai_judgment = get_text(props.get("AI原评判"))
        teacher_correction = get_text(props.get("老师正确纠正"))

        # 尝试从AI评判中提取Band分数
        ai_band = extract_band_from_text(ai_judgment)
        teacher_band = props.get("最终BandScore", {}).get("number") or 0

        # 提取错误类型
        error_types = get_text(props.get("错误类型")).split(", ")

        badcases.append({
            "学生ID": get_text(props.get("学生ID")),
            "原始题目": get_text(props.get("原始题目")),
            "学生错误答案": get_text(props.get("学生错误答案")),
            "AI原评判": ai_judgment,
            "老师正确纠正": teacher_correction,
            "错误类型": error_types,
            "AI_band": ai_band,
            "Teacher_band": teacher_band,
            "Band误差": abs(ai_band - teacher_band) if ai_band > 0 else None,
            "时间戳": get_text(props.get("时间戳")),
        })

    return badcases

def extract_band_from_text(text: str) -> float:
    """从文本中提取Band分数"""
    import re
    if not text:
        return 0.0

    # 匹配各种Band格式
    patterns = [
        r"Band Score[：:]*\s*(\d+\.?\d*)",
        r"Band[：:]*\s*(\d+\.?\d*)",
        r"综合\s*(\d+\.?\d*)",
        r"(\d+\.?\d*)\s*/\s*9\.?0?",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                continue

    return 0.0

def calculate_metrics(badcases: list) -> dict:
    """计算评估指标"""
    if not badcases:
        return {
            "sample_count": 0,
            "message": "本周暂无已纠正的样本"
        }

    metrics = {
        "sample_count": len(badcases),
        "band_error": {},
        "dimension_accuracy": defaultdict(lambda: {"correct": 0, "total": 0}),
        "error_hit_rate": {"detected": 0, "actual": 0},
    }

    total_band_error = 0
    valid_band_errors = 0

    # 统计Band误差
    band_errors = []
    for bc in badcases:
        if bc["Band误差"] is not None and bc["Band误差"] > 0:
            band_errors.append(bc["Band误差"])
            total_band_error += bc["Band误差"]
            valid_band_errors += 1

    if valid_band_errors > 0:
        metrics["band_error"] = {
            "avg": round(total_band_error / valid_band_errors, 2),
            "max": round(max(band_errors), 2),
            "min": round(min(band_errors), 2),
            "valid_samples": valid_band_errors
        }
    else:
        metrics["band_error"] = {"avg": 0, "max": 0, "min": 0, "valid_samples": 0}

    # 统计各维度准确率
    # 从老师纠正中判断AI是否漏识别了错误
    for bc in badcases:
        error_types = bc["错误类型"]
        if not error_types or error_types == [""]:
            continue

        for error_type in error_types:
            if error_type in ["语法", "词汇", "时态", "逻辑", "思路"]:
                # 检查AI评判中是否提到了这个错误
                if error_type in bc["AI原评判"] or error_type in bc["老师正确纠正"]:
                    # 如果老师纠正了，说明AI没识别到或识别错了
                    if error_type in bc["老师正确纠正"] and error_type not in bc["AI原评判"]:
                        metrics["dimension_accuracy"][error_type]["total"] += 1
                        # AI漏识别
                    elif error_type in bc["AI原评判"]:
                        metrics["dimension_accuracy"][error_type]["correct"] += 1
                        metrics["dimension_accuracy"][error_type]["total"] += 1

    # 计算各维度准确率
    for dim in metrics["dimension_accuracy"]:
        total = metrics["dimension_accuracy"][dim]["total"]
        correct = metrics["dimension_accuracy"][dim]["correct"]
        if total > 0:
            metrics["dimension_accuracy"][dim]["accuracy"] = round(correct / total * 100, 1)
        else:
            metrics["dimension_accuracy"][dim]["accuracy"] = None

    return metrics

def format_report(metrics: dict, badcases: list) -> str:
    """格式化评估报告"""
    lines = []
    lines.append("=" * 60)
    lines.append("📊 每周AI评分评估报告")
    lines.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 60)

    if metrics.get("sample_count", 0) == 0:
        lines.append("\n⚠️ 本周暂无已纠正的样本")
        lines.append("\n提示：老师的每一次/纠正都是评估数据")
        return "\n".join(lines)

    lines.append(f"\n📈 样本概览")
    lines.append(f"  • 评估样本数：{metrics['sample_count']}条")
    lines.append(f"  • 有效Band对比：{metrics['band_error'].get('valid_samples', 0)}条")

    # Band误差
    lines.append(f"\n🎯 Band评分准确率")
    be = metrics.get("band_error", {})
    if be.get("avg") is not None:
        avg_error = be["avg"]
        status = "✅ 达标" if avg_error <= 0.3 else "⚠️ 偏高"
        lines.append(f"  • 平均误差：{avg_error}（目标≤0.3）{status}")
        lines.append(f"  • 最大误差：{be['max']}")
        lines.append(f"  • 最小误差：{be['min']}")
    else:
        lines.append("  • 暂无有效数据")

    # 各维度准确率
    lines.append(f"\n📝 各维度准确率")
    dim_order = ["语法", "词汇", "时态", "逻辑", "思路"]
    dim_metrics = metrics.get("dimension_accuracy", {})

    for dim in dim_order:
        if dim in dim_metrics:
            dm = dim_metrics[dim]
            if dm.get("accuracy") is not None:
                acc = dm["accuracy"]
                status = "✅" if acc >= 85 else "⚠️" if acc >= 70 else "❌"
                lines.append(f"  {status} {dim}：{acc}%（目标≥85%）")
            else:
                lines.append(f"  ➖ {dim}：数据不足")
        else:
            lines.append(f"  ➖ {dim}：暂无数据")

    # 问题汇总
    lines.append(f"\n💡 问题与改进建议")

    avg_error = metrics.get("band_error", {}).get("avg", 0)
    if avg_error > 0.5:
        lines.append("  • Band评分系统性偏高/偏低，建议检查评分Prompt校准规则")
    elif avg_error > 0.3:
        lines.append("  • Band误差略高，可关注具体样本优化Prompt")

    weak_dims = [(dim, dm["accuracy"]) for dim, dm in dim_metrics.items()
                 if dm.get("accuracy", 0) < 85]
    if weak_dims:
        lines.append(f"  • 维度准确率偏低：{', '.join([d[0] for d in weak_dims])}")
        lines.append("    建议：增加该维度的评判规则和示例")

    lines.append("\n" + "=" * 60)

    return "\n".join(lines)

def evaluate(days: int = 7) -> dict:
    """
    主评估函数

    Args:
        days: 评估最近N天的数据

    Returns:
        dict: 评估结果
    """
    print(f"正在获取最近{days}天的错题本记录...")

    # 1. 获取数据
    badcases = get_recent_badcases(days=days)
    print(f"获取到{len(badcases)}条记录")

    # 2. 计算指标
    metrics = calculate_metrics(badcases)

    # 3. 生成报告
    report = format_report(metrics, badcases)

    return {
        "metrics": metrics,
        "badcases": badcases,
        "report": report
    }

if __name__ == "__main__":
    # 支持自定义天数
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 7

    result = evaluate(days=days)

    print(result["report"])

    # 输出详细数据（供调试）
    print("\n--- 详细数据 ---")
    print(json.dumps({
        "metrics": result["metrics"],
        "sample_count": len(result["badcases"])
    }, ensure_ascii=False, indent=2))
