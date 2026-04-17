# ielts-speaking-ai
# 雅思口语 AI 助教系统

> 🎓 面向雅思口语教师的 AI 助教系统 —— 让老师专注于教学，从重复性评分工作中解放。

[![GitHub stars](https://img.shields.io/github/stars/KaichenCurry/ielts-speaking-ai?style=flat-square)](https://github.com/KaichenCurry/ielts-speaking-ai/stargazers)
[![MIT License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)](https://www.python.org/)

**[🇬🇧 English](README_en.md)** | **🇨🇳 中文介绍**

---

## 📌 这是什么？

一个完整的 AI 驱动的雅思口语练习与评测系统，专为雅思口语教师设计。老师一条指令布置作业，学生在家语音答题，系统自动完成评分、个性化反馈、Notion 存档和周报推送。

**目标用户：雅思口语教师**

---

## 😤 痛点

| 痛点 | 现状 | 影响 |
|------|------|------|
| 重复性评分工作繁重 | 每次作业都要手动批改 | 花费数小时评分，而非教学设计 |
| 反馈严重滞后 | 学生次日甚至更久才收到反馈 | 错失最佳记忆窗口 |
| 数据散落丢失 | 学生记录难以追踪 | 无法形成系统化教学档案 |
| 班级进度黑盒 | 手动统计费时费力 | 难以针对性调整教学策略 |

---

## 💡 我们的解决方案

```
老师发送 → /题目 Test 07    （一条指令）
        ↓
系统自动发送 Part 1/2/3 全部题目给学生
        ↓
学生在家语音答题
        ↓
AI 自动评分 → 即时逐句反馈
        ↓
数据存档 Notion + 每周五推送周报
```

**核心价值**：老师从"评分员"变成"教学干预者"

---

## ✨ 五大核心功能

### 1️⃣ 一键布置作业
```
/题目 Test 07
```
一条指令，66 套真题随时调用，Part 1/2/3 全部题目自动发送。

### 2️⃣ AI 自动评测

**技术架构**：

| 环节 | 技术选型 | 为什么选它 |
|------|---------|-----------|
| 语音识别 | **Whisper** (OpenAI) | 当前最先进的开源语音识别模型，支持本地运行 |
| 评分推理 | **MiniMax** (通过 OpenClaw) | 原生中文理解能力强，性价比高，与 OpenClaw 无缝集成 |
| 上下文增强 | **RAG** | 融合历史错题，提升评分准确性 |

> **为什么选 MiniMax？**  
> MiniMax 通过 OpenClaw 网关 API 集成，具备原生中文理解能力，对雅思口语评分场景优化，同时成本效益高，适合教育场景。

> **为什么选 Whisper？**  
> OpenAI 的 Whisper 是当前语音识别领域的最先进模型，开源可本地运行，多语言支持优秀，能有效处理各种口音的英语。

### 3️⃣ 逐句多维度反馈

每句话都从 5 个维度分析：

| 维度 | 关注点 |
|------|--------|
| 语法 | 主谓一致、从句使用、介词搭配 |
| 词汇 | Chinglish、同义词替换、高分词汇 |
| 时态 | 过去时、现在时、完成时 |
| 逻辑 | 因果关系、转折、层次感、跑题 |
| 思路 | 举例是否具体、论证深度、独特观点 |

### 4️⃣ Notion 数据存档

📎 **Notion 数据库链接**：
- [题库](https://www.notion.so/bba82871-4fe1-4409-9f70-72f6bf27e7b3) - 66 套真题
- [作业反馈库](https://www.notion.so/3412e55d-7136-8179-9ac8-ee60a420ac21) - 练习存档
- [错题本](https://www.notion.so/3412e55d-7136-8113-aa98-cfd36af9799c) - 错误案例

### 5️⃣ 班级周报推送

每周五 18:00 自动推送到 Telegram 群

```
📊 班级周报 | 2026.04.11-04.15

【练习概览】
• 练习人次：12
• 平均 Band：6.2
• 较上周变化：+0.3 ↑

【Band 分布】
• 7.0+：3人
• 6.0-6.5：6人
• 5.5-6.0：2人

【常见错误 TOP5】
1. 时态混用 —— 8次
2. 主谓不一致 —— 6次
3. 举例与观点不匹配 —— 5次
```

---

## 🏗️ 系统架构

```
┌──────────────────────────────────────────────────────────┐
│                    老师操作界面                            │
│     /题目 Test XX  →  /纠正  →  查看 Notion  →  周报   │
└──────────────────────────────────────────────────────────┘
                           ↓ Telegram Bot
┌──────────────────────────────────────────────────────────┐
│                     AI 评测流水线                        │
│                                                          │
│   🎤 语音  →  Whisper  →  RAG  →  MiniMax  →  📊 评分  │
│                                                          │
└──────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────┐
│                     数据存储层                            │
│              Notion（题库 / 作业库 / 错题本）             │
└──────────────────────────────────────────────────────────┘
```

### Band Score 计算公式

```
综合 Band = Part1×30% + (Part2×40% + Part3×60%)×70%
```

计算示例：
```
Part1 均分 = 6.0, Part2 = 6.5, Part3 均分 = 6.0
Part2_3 合成 = 6.5×0.4 + 6.0×0.6 = 6.2
综合 Band = 6.0×0.3 + 6.2×0.7 = 6.14 ≈ 6.0
```

---

## 📊 效果指标

> ⚠️ **可信度说明**：基于 2026-04 运营数据（20+ 次练习），仅供参考。

| 指标 | 目标 | 实际 | 样本量 |
|------|------|------|--------|
| Band 评分误差 | ≤0.3 | **0.2** | 20+ 次 |
| 格式正确率 | ≥98% | **98%+** | 每周抽样 |

---

## 🚀 快速部署

### 1. 克隆项目

```bash
git clone https://github.com/KaichenCurry/ielts-speaking-ai.git
cd ielts-speaking-ai
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填写实际 Token
```

### 4. 运行

```bash
# 初始化会话
python3 scripts/ielts_flow.py init '{"test_number": 7, "Part 1": ["Q1", "Q2"], "Part 2 题卡": "Describe a shopping mall", "Part 3": ["Q1", "Q2"]}'

# 处理学生音频（自动转写+评分）
python3 scripts/ielts_flow.py process /path/to/audio.wav
```

---

## 📖 真实 Demo

### 学生答题 → AI 反馈

**学生原音转写**：
> "Definitely, yes, reading has been my hobby since I was a child and I've been a catering story books for fun, but now I'm preparing for my studies abroad and shifted to reading academic articles and biographies of influential figures. It's a total problem of horizons and improve my vocabulary."

**AI 逐句反馈**：

| 原句 | 维度 | 诊断 | 建议 |
|------|------|------|------|
| "reading has been my hobby since I was a child" | ✅ 时态 | 表达自然 | — |
| "I've been a catering story books for fun" | ❌ 词汇 | "catering" 词性误用 | → "reading story books for fun" |
| "shifted to reading academic articles" | ✅ 词汇 | "shifted to" 使用准确 | — |
| "It's a total problem of horizons" | ❌ 词汇 | Chinglish | → "It's really broadened my horizons" |

**评分结果**：Band Score 6.0 / 9.0

---

## 📁 项目结构

```
ielts-speaking-ai/
├── README_en.md              # 🇬🇧 English version
├── README_zh.md              # 🇨🇳 中文介绍（本文件）
│
├── docs/
│   ├── SYSTEM_DESIGN.md     # 详细技术文档
│   └── PORTFOLIO_RESUME.md  # 简历 & 作品集
│
├── scripts/
│   ├── ielts_flow.py        # ⭐ 主流程控制器
│   ├── answer_flow.py       # ⭐ 状态机
│   ├── analyze_transcript.py # ⭐ AI 评分
│   ├── rag_retrieve.py      # ⭐ RAG 检索
│   ├── notion_search.py      # Notion 题库搜索
│   ├── notion_append_homework.py  # 作业存档
│   ├── topic_updater.py      # 题库自动更新
│   └── weekly_report.py      # 周报生成
│
└── references/
    ├── prompts.md           # 评分 Prompt 模板
    └── prompt_changelog.md   # Prompt 迭代日志
```

---

## 🔄 数据飞轮

```
学生答题 → AI评分 → 老师纠正 → 错题本收录 → RAG增强 → 微调数据
```

每一次老师纠正都是高质量标注数据。当错题本积累到 100+ 条后，可启动模型微调。

---

## 👤 作者

**Curry Chen**  
雅思口语教师 / AI 产品探索者

- GitHub: [@KaichenCurry](https://github.com/KaichenCurry)
- 项目链接: https://github.com/KaichenCurry/ielts-speaking-ai

---

<p align="center">
  <strong>如果这个项目对你有帮助，请点个 ⭐ Star！</strong>
</p>
