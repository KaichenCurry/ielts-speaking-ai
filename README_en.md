# 🎓 ielts-speaking-ai
# 雅思口语 AI 助教系统

> 让老师专注于教学，从重复性评分工作中解放。

[![Stars](https://img.shields.io/github/stars/KaichenCurry/ielts-speaking-ai?style=flat-square)](https://github.com/KaichenCurry/ielts-speaking-ai/stargazers)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)](https://www.python.org/)
[![Last Commit](https://img.shields.io/github/last-commit/KaichenCurry/ielts-speaking-ai?style=flat-square)](https://github.com/KaichenCurry/ielts-speaking-ai/commits)

🌐 **Language**: 🇺🇸 **English** | [🇨🇳 中文介绍](README.md)

---

## 📋 Table of Contents

- [🎯 What is this?](#-what-is-this)
- [😤 The Problem](#-the-problem)
- [💡 Our Solution](#-our-solution)
- [🏗️ Tech Stack](#️-tech-stack)
- [✨ Features](#-features)
- [📖 Demo](#-demo)
- [🚀 Quick Start](#-quick-start)
- [📁 Project Structure](#-project-structure)
- [🗺️ Roadmap](#️-roadmap)
- [👤 Author](#-author)

---

## 🎯 What is this?

An **AI-powered IELTS speaking practice & evaluation system** designed for IELTS speaking teachers.

```
Teacher types:  /题目 Test 07
        ↓
System sends Part 1/2/3 questions
        ↓
Student records voice answers at home
        ↓
AI auto-scores → Instant sentence-by-sentence feedback
        ↓
Data archived to Notion + Weekly report every Friday
```

**Target User: IELTS Speaking Teachers**

---

## 😤 The Problem

| Pain Point | Reality | Impact |
|-----------|---------|--------|
| 🔴 Repetitive grading | Manually scoring every homework | Hours spent on grading, not teaching |
| 🔴 Delayed feedback | Students wait a day for results | Miss the optimal learning window |
| 🔴 Scattered data | Student progress hard to track | Can't build systematic archives |
| 🔴 No class overview | Manual statistics are time-consuming | Difficult to adjust teaching strategies |

---

## 💡 Our Solution

### Before vs After

```
┌─────────────────────────────────────────────────────────────────┐
│                        BEFORE (Manual)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Teacher: "Grade 20 homeworks"                                  │
│       ↓                                                          │
│  ⏱️ 3 hours of repetitive scoring                               │
│       ↓                                                          │
│  Student: "When will I get feedback?"                            │
│       ↓                                                          │
│  📝 Paper scattered, no data, no tracking                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

                              ↓ ielts-speaking-ai ↓

┌─────────────────────────────────────────────────────────────────┐
│                        AFTER (AI-Powered)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Teacher: "/题目 Test 07"  ← one command                      │
│       ↓                                                          │
│  ✅ System sends questions automatically                         │
│       ↓                                                          │
│  Student: records voice → gets instant feedback                 │
│       ↓                                                          │
│  📊 Notion archived + Friday weekly report                      │
│       ↓                                                          │
│  Teacher: Focus on real teaching intervention                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Tech Stack

> **Why these three? Together they form the perfect AI teaching assistant.**

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│   📱 Telegram          +   🤖 OpenClaw          +   📋 Notion  │
│   ──────────────           ─────────────           ───────────  │
│                                                                  │
│   🌐 Instant Message      🧠 AI Agent Core      📊 Data Storage  │
│   Native voice support   Multi-model fusion    Structured docs  │
│   Multi-platform        Native Chinese         Scalable archive  │
│   Low barrier           Mature platform        Teacher-friendly  │
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  🎤 Voice → 📝 Whisper → 🧠 MiniMax → 📊 Band Score  │   │
│   │              ↑ OpenClaw Agent orchestration ↑           │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Why Telegram?

| Advantage | Explanation |
|-----------|-------------|
| 🌐 Native voice support | Telegram supports voice messages natively, perfect for speaking practice |
| 🌍 Multi-language | Built-in translation, great for international students |
| 📱 Cross-platform | iOS/Android/Desktop, students can practice anywhere |
| 🔔 Instant notifications | Students get questions immediately |
| 📊 Group features | Built-in group reports, weekly summaries |

### Why OpenClaw?

| Advantage | Explanation |
|-----------|-------------|
| 🧠 Mature AI Agent | Native Whisper + MiniMax + RAG integration |
| 🔄 Workflow automation | State machine for Part 1→2→3 flow |
| 🌐 Chinese-native | Excellent Chinese context understanding |
| 💰 Cost-effective | Compared to GPT-4, better for education scenarios |

### Why Notion?

| Advantage | Explanation |
|-----------|-------------|
| 📊 Structured data | Question bank, homework archive, error cases |
| 📝 Teacher-friendly | No-code database, easy for non-tech teachers |
| 🔗 API integration | Auto-archive homework, searchable |
| 📈 Progress tracking | Student growth over time |

---

## ✨ Features

### 1️⃣ One-Click Assignment
```
/题目 Test 07

✅ Part 1 sent (5 questions)
✅ Part 2 sent (Cue Card)
✅ Part 3 sent (5 questions)
```
66 real exam questions, ready to use.

### 2️⃣ AI Auto-Scoring

| Component | Technology | Function |
|-----------|------------|----------|
| 🎤 Speech-to-Text | **Whisper** (OpenAI) | Voice → Text |
| 📚 Context | **RAG** | Historical errors enhance scoring |
| 🧠 Scoring | **MiniMax** (via OpenClaw) | 5-dimension evaluation |
| 📊 Band Calc | **Formula** | Part1×30% + (Part2×40%+Part3×60%)×70% |

### 3️⃣ 5-Dimension Feedback

| Dimension | Focus | Example Issue |
|-----------|-------|--------------|
| 📝 Grammar | Subject-verb, clauses | "He go" → "He goes" |
| 📖 Vocabulary | Chinglish, synonyms | "很贵" → "expensive" |
| ⏰ Tense | Past/present/perfect | Past events in present tense |
| 🔗 Logic | Causality, transitions |观点与举例不匹配 |
| 💡 Ideas | Examples, depth | 举例泛泛而谈 |

### 4️⃣ Notion Integration

📎 **Databases**:
- [Question Bank](https://www.notion.so/bba82871-4fe1-4409-9f70-72f6bf27e7b3) - 66 exam sets
- [Homework Archive](https://www.notion.so/3412e55d-7136-8179-9ac8-ee60a420ac21) - Practice records
- [Error Cases](https://www.notion.so/3412e55d-7136-8113-aa98-cfd36af9799c) - Historical mistakes

### 5️⃣ Weekly Reports

Every Friday 18:00 → Auto-push to Telegram

```
📊 Weekly Report | Apr 11-15

【Practice Overview】
• Sessions: 12
• Average Band: 6.2
• Change: +0.3 ↑

【Band Distribution】
• 7.0+: 3 students ████
• 6.0-6.5: 6 students ████████████
• 5.5-6.0: 2 students ████

【Common Errors TOP 5】
1. Tense mixing — 8 times
2. Subject-verb — 6 times
```

---

## 📖 Demo

### Student Answer → AI Feedback

**Original transcript**:
> "Definitely, yes, reading has been my hobby since I was a child and I've been a catering story books for fun, but now I'm preparing for my studies abroad and shifted to reading academic articles..."

**AI Sentence-by-Sentence Feedback**:

| Sentence | Grammar | Vocabulary | Tense | Logic | Ideas |
|----------|---------|------------|-------|-------|-------|
| "reading has been my hobby since I was a child" | ✅ | ✅ | ✅ | ✅ | ✅ |
| "I've been a catering story books" | ✅ | ❌ `catering` → `reading` | ✅ | ✅ | ✅ |
| "shifted to reading academic articles" | ✅ | ✅ | ✅ | ✅ | ✅ |
| "It's a total problem of horizons" | ✅ | ❌ Chinglish → `broadened my horizons` | ✅ | ✅ | ✅ |

**Result**: Band Score **6.0 / 9.0**

---

## 📊 Metrics

> ⚠️ **Disclaimer**: Based on limited operational data (20+ sessions, April 2026).

| Metric | Target | Actual | Sample |
|--------|--------|--------|--------|
| Band Error | ≤0.3 | **0.2** | 20+ |
| Format Accuracy | ≥98% | **98%+** | Weekly |

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
# Edit .env with your tokens
```

```bash
# Required tokens:
TELEGRAM_BOT_TOKEN=your_bot_token      # From @BotFather
MINIMAX_API_KEY=your_api_key          # Via OpenClaw gateway
NOTION_TOKEN=your_notion_token         # From notion.so/my-integrations
NOTION_QUESTION_DB_ID=your_db_id      # Question bank database ID
NOTION_HOMEWORK_DB_ID=your_db_id      # Homework archive database ID
NOTION_BADCASE_DB_ID=your_db_id       # Error cases database ID
```

### 4. Run

```bash
# Initialize session
python3 scripts/ielts_flow.py init '{"test_number": 7, "Part 1": ["Q1", "Q2"], "Part 2 题卡": "Describe a shopping mall", "Part 3": ["Q1", "Q2"]}'

# Process student audio (auto transcript + scoring)
python3 scripts/ielts_flow.py process /path/to/audio.wav
```

---

## 📁 Project Structure

```
ielts-speaking-ai/
│
├── 📄 README.md                # 🇨🇳 Chinese version (default)
├── 📄 README_en.md              # 🇺🇸 English version (this file)
│
├── 🔧 Core Scripts
│   ├── ielts_flow.py          # ⭐ Main controller (Whisper+MiniMax+RAG)
│   ├── answer_flow.py          # ⭐ State machine (Part1→2→3)
│   ├── analyze_transcript.py   # ⭐ AI scoring analysis
│   └── rag_retrieve.py         # ⭐ RAG retrieval
│
├── 📱 Platform Integration
│   ├── notion_search.py         # Notion question bank
│   ├── notion_append_homework.py # Homework archive
│   └── notion_append_badcase.py  # Error cases
│
├── 🔄 Automation
│   ├── topic_updater.py         # Auto question bank update
│   ├── weekly_report.py          # Weekly report generation
│   └── evaluate_weekly.py        # Weekly evaluation
│
└── 📚 Documentation
    ├── docs/SYSTEM_DESIGN.md    # Detailed technical docs
    └── docs/PORTFOLIO_RESUME.md # Resume & portfolio
```

---

## 🗺️ Roadmap

### Current Version ✅
```
┌─────────────────────────────────────────────────────┐
│                   Current: v1.0                      │
├─────────────────────────────────────────────────────┤
│                                                      │
│  📱 Telegram Bot                                     │
│  🤖 OpenClaw Agent (MiniMax + Whisper)              │
│  📋 Notion Integration                              │
│                                                      │
│  ✅ Voice practice                                   │
│  ✅ AI auto-scoring                                 │
│  ✅ Sentence-by-sentence feedback                     │
│  ✅ Notion archival                                 │
│  ✅ Weekly reports                                   │
│  ✅ 66 question bank                                │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Future Versions 🔜

```
┌─────────────────────────────────────────────────────┐
│                   Roadmap                            │
├─────────────────────────────────────────────────────┤
│                                                      │
│  v1.1 (Q2 2026)                                     │
│  ├── 🔜 WeChat Mini Program integration              │
│  ├── 🔜 Feishu/Lark Bot integration                 │
│  └── 🔜 Enterprise WeChat integration               │
│                                                      │
│  v1.2 (Q3 2026)                                    │
│  ├── 🔜 Hermes Agent (OpenClaw's next-gen)          │
│  ├── 🔜 Multi-agent orchestration                   │
│  └── 🔜 Advanced RAG with vector search             │
│                                                      │
│  v2.0 (Q4 2026)                                    │
│  ├── 🔜 Feishu Docs integration                     │
│  ├── 🔜 Tencent Docs integration                    │
│  ├── 🔜 Fine-tuning with accumulated data          │
│  └── 🔜 Student progress dashboard                  │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Why Expand to WeChat/Feishu?

| Platform | Advantage for This Project |
|---------|---------------------------|
| 💬 **WeChat** | 1.2B+ users, dominant in China, students already have it |
| 📱 **Feishu/Lark** | Great for corporate/education, built-in calendar |
| 🏢 **Enterprise WeChat** | For language schools with existing WeCom infrastructure |
| 📄 **Feishu/Tencent Docs** | Replace Notion for teams already using these tools |

---

## 🔄 Data Flywheel

```
Student Practice → AI Scoring → Teacher Correction → Error Cases → RAG Enhancement → Fine-tuning
```

Every teacher correction is high-quality labeled data.
When error cases reach 100+, model fine-tuning becomes possible.

---

## 👤 Author

**Curry Chen**  
IELTS Speaking Teacher / AI Product Explorer

| Platform | Link |
|----------|------|
| 🌐 GitHub | [@KaichenCurry](https://github.com/KaichenCurry) |
| 📂 Project | https://github.com/KaichenCurry/ielts-speaking-ai |

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

---

<p align="center">
  <strong>⭐ Star this project if you find it helpful!</strong>
</p>
