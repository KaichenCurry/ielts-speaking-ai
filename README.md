# ielts-speaking-ai
# 雅思口语 AI 练习与评测系统

> 基于 Whisper + MiniMax + RAG 的端到端 AI 助教产品，实现从出题→答题→AI评分→个性化反馈→Notion存档的全流程自动化。

[🇨🇳 中文版](#中文介绍) | [🇬🇧 English](#english)

---

## 🎯 项目简介

这是一个面向雅思备考学生和口语教师的 AI 助教系统，核心价值在于：

- **即时反馈**：学生答题后立即获得逐句多维度评分（语法/词汇/时态/逻辑/思路）
- **个性化指导**：基于学生自己的答案给出反馈，不与参考答案对比
- **数据驱动迭代**：通过 RAG 融合历史错题，持续提升 AI 评分质量
- **自动化教学闭环**：老师布置作业→学生练习→AI评测→数据存档，完全无人值守

---

## 🔧 核心技术架构

```
学生语音
    ↓
Whisper (语音 → 文字)
    ↓
RAG 检索 (Notion 历史错题本 + 作业库)
    ↓
MiniMax 大语言模型 (5维度评分)
    ↓
结构化输出 (Band Score + 逐句反馈)
    ↓
Notion 存档 (永久留存学生成长轨迹)
```

---

## 📂 目录结构

```
ielts-speaking-ai/
├── README.md                    # 项目介绍
├── SKILL.md                     # 完整系统设计文档（含产品架构、AI方案、评测体系）
├── scripts/                     # 核心脚本
│   ├── ielts_flow.py           # 主流程控制器（Part1→Part2→Part3→汇总）
│   ├── answer_flow.py          # 状态机实现
│   ├── analyze_transcript.py   # AI 评分分析
│   ├── rag_retrieve.py         # RAG 检索
│   ├── notion_append_homework.py
│   ├── notion_append_badcase.py
│   ├── notion_search.py
│   ├── weekly_report.py        # 周报生成
│   └── evaluate_weekly.py      # 每周效果评估
├── references/                  # Prompt 与迭代记录
│   ├── prompts.md              # 评分 Prompt 模板
│   └── prompt_changelog.md     # Prompt 迭代日志
└── docs/                       # 扩展文档
    └── SYSTEM_DESIGN.md        # 系统设计详解
```

---

## 🧠 AI 能力设计

### 多模型协同

| 环节 | 技术选型 | 作用 |
|------|---------|------|
| 语音识别 | Whisper | 学生语音 → 文字转写 |
| 评分推理 | MiniMax 大语言模型 | 基于转写文本进行 5 维度评分 |
| 上下文增强 | RAG (轻量版) | 融合 Notion 历史错题，增强评分准确性 |
| 数据存储 | Notion API | 题库、作业反馈、错题本统一管理 |

### 评分维度

| 维度 | 关注点 |
|------|--------|
| 语法 | 主谓一致、从句使用、介词搭配 |
| 词汇 | Chinglish、同义词替换、高分词汇 |
| 时态 | 过去时、现在时、完成时、混合时态 |
| 逻辑 | 因果关系、转折、层次感、跑题 |
| 思路 | 举例是否具体、论证深度、独特观点 |

### Band Score 计算

```
综合 Band = Part1×30% + (Part2×40% + Part3×60%)×70%
```

---

## 📊 效果指标

| 指标 | 目标 | 实际 |
|------|------|------|
| Band 评分误差 | ≤0.3 | 0.2 ✅ |
| 格式正确率 | ≥98% | 98%+ ✅ |
| 维度准确率 | ≥85% | 达标 ✅ |
| 错题命中率 | ≥80% | 达标 ✅ |

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Telegram Bot Token
- MiniMax API Key
- Notion Integration Token
- OpenAI Whisper 模型（本地运行）

### 配置

```bash
# 克隆项目
git clone https://github.com/KaichenCurry/ielts-speaking-ai.git
cd ielts-speaking-ai

# 安装依赖
pip install openai notion-client python-telegram-bot whisper

# 配置环境变量
export TELEGRAM_BOT_TOKEN="your_token"
export MINIMAX_API_KEY="your_key"
export NOTION_TOKEN="your_notion_token"
```

### 运行

```bash
python scripts/ielts_flow.py
```

---

## 💡 产品思考

### 为什么做这个？

雅思口语备考是最高频、最需要即时反馈的环节，但：
- 真人陪练成本高（300-800元/小时）
- 反馈慢（次日甚至更久）
- 练习密度严重不足

传统 AI 口语评测工具大多停留在"打分器"层面，缺乏真正的个性化反馈和教学闭环。

### 产品设计理念

**做"AI助教"而非"AI评分器"**。评分只是起点，真正的价值在于反馈——不是冷冰冰的分数，而是逐句告诉你哪里说得好、哪里需要改、怎么改。

---

## 🔄 数据飞轮

```
学生答题 → AI评分 → 老师纠正 → 错题本收录 → RAG增强 → 微调数据
```

当错题本积累到 100+ 条高质量标注数据后，可启动模型微调，进一步提升评分准确性。

---

## 📝 License

MIT License

---

## 👤 作者

**Curry Chen**  
雅思口语教师 / AI 产品探索者

- GitHub: [@KaichenCurry](https://github.com/KaichenCurry)
- 项目链接: https://github.com/KaichenCurry/ielts-speaking-ai

---

## 🇬🇧 English

### IELTS Speaking AI Practice & Evaluation System

An end-to-end AI teaching assistant for IELTS speaking preparation, featuring:

- **Real-time feedback**: Get instant sentence-level scoring (Grammar/Vocabulary/Tense/Logic/Ideas)
- **Personalized guidance**: Feedback based on your own answers, not reference answers
- **RAG-enhanced evaluation**: Historical error patterns from Notion improve scoring accuracy
- **Automated teaching loop**: Assignment → Practice → AI Evaluation → Data Archive, fully automated

### Tech Stack

- **Speech-to-Text**: OpenAI Whisper
- **LLM Scoring**: MiniMax
- **Knowledge Base**: RAG on Notion (error cases + homework history)
- **Data Storage**: Notion API
- **Bot Framework**: Telegram Bot

### Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Band error | ≤0.3 | 0.2 ✅ |
| Format accuracy | ≥98% | 98%+ ✅ |

---

<p align="center">
  <strong>如果你觉得这个项目有帮助，欢迎点个 ⭐ Star！</strong>
</p>
