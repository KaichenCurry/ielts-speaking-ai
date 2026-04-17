# ielts-speaking-ai

> 🎓 面向雅思口语教师的 AI 助教系统 —— 让老师专注于教学，从重复性评分工作中解放。

[![GitHub stars](https://img.shields.io/github/stars/KaichenCurry/ielts-speaking-ai?style=flat-square)](https://github.com/KaichenCurry/ielts-speaking-ai/stargazers)
[![MIT License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)](https://www.python.org/)

**English** | [中文介绍](#中文介绍)

---

## 📌 What is this?

A complete AI-powered IELTS speaking practice and evaluation system for teachers. Teachers assign homework with one command, students practice at home with voice recording, and the system automatically handles scoring, personalized feedback, Notion archival, and weekly reports.

**Target User: IELTS Speaking Teachers**

---

## 😤 The Problem

Teachers face daily frustrations:

| Pain Point | Reality | Impact |
|-----------|---------|--------|
| Repetitive grading | Manually scoring every student's homework | Hours spent on scoring instead of teaching |
| Delayed feedback | Students wait a day or more for results | Miss the optimal learning window |
| Scattered data | Student progress records hard to track | Can't build systematic teaching archives |
| No class overview | Manual statistics are time-consuming | Difficult to adjust teaching strategies |

---

## 💡 Our Solution

```
Teacher types → /题目 Test 07    (one command)
        ↓
System sends Part 1/2/3 questions to student
        ↓
Student records voice answers at home
        ↓
AI automatically scores → Instant sentence-by-sentence feedback
        ↓
Data archived to Notion + Weekly report every Friday
```

**Core Value**: Teachers go from "grader" to "teaching interventionist"

---

## ✨ Features

### 1️⃣ One-Click Assignment
```bash
/题目 Test 07
```
Send all Part 1/2/3 questions instantly. 66 real exam questions available.

### 2️⃣ AI Auto-Scoring

**Tech Stack**:

| Component | Technology | Why |
|-----------|------------|-----|
| Speech Recognition | **Whisper** (OpenAI) | State-of-the-art, open-source, excellent for voice-to-text |
| Scoring Model | **MiniMax** (via OpenClaw) | Native Chinese understanding, cost-effective, native integration |
| Context Enhancement | **RAG** | Historical error cases improve scoring accuracy |

> **Why MiniMax?**  
> MiniMax is integrated via OpenClaw gateway API. It offers excellent Chinese language understanding, competitive pricing, and native Agent/Workflow support — making it the natural choice for this system's LLM needs.

> **Why Whisper?**  
> OpenAI's Whisper is the current state-of-the-art for speech recognition. It's open-source, runs locally, and handles various accents well — ideal for student voice input.

### 3️⃣ Sentence-Level Feedback

5-dimension analysis per sentence:

| Dimension | Focus |
|-----------|-------|
| Grammar | Subject-verb agreement, clauses, prepositions |
| Vocabulary | Chinglish, synonyms, high-scoring words |
| Tense | Past/present/perfect |
| Logic | Causality, transitions, topic relevance |
| Ideas | Specificity of examples, depth of argument |

### 4️⃣ Notion Integration

📎 **Notion Databases**:
- [Question Bank](https://www.notion.so/bba82871-4fe1-4409-9f70-72f6bf27e7b3) - 66 exam sets
- [Homework Archive](https://www.notion.so/3412e55d-7136-8179-9ac8-ee60a420ac21) - Practice records
- [Error Cases](https://www.notion.so/3412e55d-7136-8113-aa98-cfd36af9799c) - Historical mistakes

### 5️⃣ Weekly Reports

Every Friday 18:00 → Auto-push to Telegram group

```
📊 Class Weekly Report | Apr 11-15, 2026

【Practice Overview】
• Sessions: 12
• Average Band: 6.2
• Change: +0.3 ↑

【Band Distribution】
• 7.0+: 3 students
• 6.0-6.5: 6 students

【Common Errors TOP 5】
1. Tense mixing — 8 times
2. Subject-verb disagreement — 6 times
```

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     Teacher Interface                     │
│  /题目 Test XX  →  /纠正  →  查看 Notion  →  Weekly Report │
└──────────────────────────────────────────────────────────┘
                           ↓ Telegram Bot
┌──────────────────────────────────────────────────────────┐
│                    AI Pipeline                            │
│                                                          │
│  🎤 Voice  →  Whisper  →  RAG  →  MiniMax  →  📊 Score │
│                                                          │
└──────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────┐
│                    Data Layer                             │
│           Notion (Question Bank / Homework / Errors)     │
└──────────────────────────────────────────────────────────┘
```

### Band Score Formula

```
Overall Band = Part1×30% + (Part2×40% + Part3×60%)×70%
```

Example:
```
Part1 avg = 6.0, Part2 = 6.5, Part3 avg = 6.0
Part2_3 = 6.5×0.4 + 6.0×0.6 = 6.2
Overall = 6.0×0.3 + 6.2×0.7 = 6.14 ≈ 6.0
```

---

## 📊 Metrics

> ⚠️ **Disclaimer**: Based on limited operational data (20+ sessions, April 2026), for internal iteration reference only.

| Metric | Target | Actual | Sample | Note |
|--------|--------|--------|--------|------|
| Band Error | ≤0.3 | **0.2** | 20+ sessions | AI Band vs teacher-confirmed Band |
| Format Accuracy | ≥98% | **98%+** | Weekly sampling | Output format consistency |

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/KaichenCurry/ielts-speaking-ai.git
cd ielts-speaking-ai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env with your tokens:

# Telegram Bot Token (from @BotFather)
TELEGRAM_BOT_TOKEN=your_bot_token

# MiniMax API Key (via OpenClaw gateway)
MINIMAX_API_KEY=your_api_key

# Notion Integration Token
NOTION_TOKEN=your_notion_token
NOTION_QUESTION_DB_ID=your_question_db_id
NOTION_HOMEWORK_DB_ID=your_homework_db_id
NOTION_BADCASE_DB_ID=your_badcase_db_id
```

### 4. Run

```bash
# Initialize session
python3 scripts/ielts_flow.py init '{"test_number": 7, "Part 1": ["Q1", "Q2"], "Part 2 题卡": "Describe a shopping mall", "Part 3": ["Q1", "Q2"]}'

# Process student audio (auto transcript + scoring)
python3 scripts/ielts_flow.py process /path/to/audio.wav
```

---

## 📖 Real Demo

### Student Answer → AI Feedback

**Original transcript**:
> "Definitely, yes, reading has been my hobby since I was a child and I've been a catering story books for fun, but now I'm preparing for my studies abroad and shifted to reading academic articles and biographies of influential figures. It's a total problem of horizons and improve my vocabulary."

**AI Sentence-by-Sentence Feedback**:

| Sentence | Dimension | Diagnosis | Suggestion |
|----------|-----------|-----------|------------|
| "reading has been my hobby since I was a child" | ✅ Tense | Natural | — |
| "I've been a catering story books for fun" | ❌ Vocabulary | "catering" misused | → "reading story books for fun" |
| "shifted to reading academic articles" | ✅ Vocabulary | Accurate | — |
| "It's a total problem of horizons" | ❌ Vocabulary | Chinglish | → "It's really broadened my horizons" |

**Result**: Band Score 6.0 / 9.0

---

## 📁 Project Structure

```
ielts-speaking-ai/
├── README.md                   # This file
├── SKILL.md                    # System design document
│
├── docs/
│   ├── SYSTEM_DESIGN.md       # Detailed technical docs
│   └── PORTFOLIO_RESUME.md    # Resume & portfolio content
│
├── scripts/
│   ├── ielts_flow.py         # ⭐ Main controller (Whisper+MiniMax+RAG)
│   ├── answer_flow.py         # ⭐ State machine
│   ├── analyze_transcript.py  # ⭐ AI scoring
│   ├── rag_retrieve.py        # ⭐ RAG retrieval
│   │
│   ├── notion_search.py        # Notion question bank search
│   ├── notion_append_homework.py # Homework archival
│   ├── notion_append_badcase.py  # Error case archival
│   │
│   ├── topic_updater.py        # Auto question bank update
│   ├── weekly_report.py        # Weekly report generation
│   └── evaluate_weekly.py      # Weekly evaluation
│
└── references/
    ├── prompts.md             # Scoring prompt templates
    └── prompt_changelog.md    # Prompt iteration log
```

---

## 🔄 Data Flywheel

```
Student Practice → AI Scoring → Teacher Correction → Error Cases → RAG Enhancement → Fine-tuning Data
```

Every teacher correction is high-quality labeled data. When error cases reach 100+, model fine-tuning becomes possible.

---

## 👤 Author

**Curry Chen**  
IELTS Speaking Teacher / AI Product Explorer

- GitHub: [@KaichenCurry](https://github.com/KaichenCurry)
- Project: https://github.com/KaichenCurry/ielts-speaking-ai

---

## 🇨🇳 中文介绍

### 雅思口语 AI 助教系统

面向雅思口语教师的 AI 辅助教学工具，帮助老师：

- ✅ **一键布置作业**：66 套真题，随时调用
- ✅ **AI 自动评测**：Whisper + MiniMax + RAG，逐句多维度反馈
- ✅ **Notion 存档**：学生数据永久留存
- ✅ **周报推送**：每周五自动推送班级全景报告
- ✅ **题库更新**：每周三、六定时自动更新

### 技术亮点

- 多模型协同（Whisper + MiniMax + RAG）
- 三段式状态机（Part 1→Part 2→Part 3）
- Band 评分误差 ≤0.3
- 数据飞轮设计，持续自我进化

### 为什么选择 MiniMax？

MiniMax 通过 OpenClaw 网关 API 集成，具备以下优势：
- **原生中文理解**：对雅思口语评分场景优化
- **成本效益**：相比 GPT-4 等更具性价比
- **OpenClaw 集成**：与 Whisper、Notion 等无缝协作

### 为什么选择 Whisper？

OpenAI 的 Whisper 是当前语音识别领域的最先进模型：
- **开源**：可本地运行，无 API 费用
- **准确性高**：在多个基准测试中表现最佳
- **多语言支持**：适合处理各种口音的英语

---

<p align="center">
  <strong>⭐ Star this project if you find it helpful!</strong>
</p>
