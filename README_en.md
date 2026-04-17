# 🎓 ielts-speaking-ai
# IELTS Speaking AI Assistant

> Auto-grades for teachers, so they can focus on teaching.

[![Stars](https://img.shields.io/github/stars/KaichenCurry/ielts-speaking-ai?style=flat-square)](https://github.com/KaichenCurry/ielts-speaking-ai/stargazers)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)](https://www.python.org/)
[![Last Commit](https://img.shields.io/github/last-commit/KaichenCurry/ielts-speaking-ai?style=flat-square)](https://github.com/KaichenCurry/ielts-speaking-ai/commits)

🌐 **Language**: 🇺🇸 **English** | [🇨🇳 中文介绍](README.md)

---

## One-Sentence Intro

An AI grading tool for **IELTS speaking teachers**.

Teacher sends one command, student practices with voice, system auto-grades with sentence-by-sentence feedback, archived to Notion.

---

## Problem Solved

| Before | After |
|--------|-------|
| Manual grading, 3 hours per assignment | AI auto-grades, 0 seconds |
| Students wait a day for feedback | Instant feedback after practice |
| Data scattered in WeChat/email | Auto-archived to Notion |

---

## How It Works (3 Steps)

```
Step 1: Teacher sends command
        ↓
Command: /题目 Test 07

Step 2: Student practices
        ↓
🎤 Voice answer → AI auto-grades

Step 3: Feedback received
        ↓
💬 Sentence feedback (Grammar/Vocabulary/Tense/Logic/Ideas)
📊 Band Score
📋 Auto-archive to Notion
```

---

## Results

| Metric | Value |
|--------|-------|
| Teacher time saved | 80%+ |
| Band score error | 0.2 |
| Format accuracy | 98%+ |

> Based on April 2026 data (20+ sessions)

---

## Tech Stack

| Component | Technology | Why |
|-----------|------------|-----|
| Message entry | Telegram | Native voice support |
| AI inference | MiniMax (OpenClaw) | Great Chinese understanding |
| Speech-to-text | Whisper | Best for spoken English |
| Data storage | Notion | Teachers use it directly |

```
Voice → Whisper → MiniMax → Score → Notion
```

---

## 5 Key Features

### 1️⃣ Assign Homework
One command sends Part 1/2/3, 66 exam questions ready

### 2️⃣ AI Auto-Grading
5-dimension feedback: Grammar / Vocabulary / Tense / Logic / Ideas

### 3️⃣ Instant Feedback
Results immediately after practice, no waiting

### 4️⃣ Notion Archive
Student history permanently stored, always accessible

### 5️⃣ Weekly Reports
Auto-push class overview every Friday

---

## Real Example

**Student Answer**:
> "I've been a catering story books for fun... It's a total problem of horizons"

**AI Feedback**:
| Issue | Diagnosis |
|-------|-----------|
| "catering story books" | Vocabulary error → "reading story books" |
| "total problem of horizons" | Chinglish → "broadened my horizons" |

**Band Score**: 6.0 / 9.0

---

## Project Structure

```
ielts-speaking-ai/
├── scripts/                    # Core code
│   ├── ielts_flow.py         # Main controller
│   ├── answer_flow.py         # State machine
│   ├── analyze_transcript.py # AI scoring
│   └── rag_retrieve.py       # RAG retrieval
├── docs/
│   ├── SYSTEM_DESIGN.md      # Technical docs
│   └── PORTFOLIO_RESUME.md   # Resume content
└── references/
    └── prompts.md            # Prompt templates
```

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/KaichenCurry/ielts-speaking-ai.git
cd ielts-speaking-ai

# 2. Install
pip install -r requirements.txt

# 3. Configure
cp .env.example .env
# Fill in your tokens

# 4. Run
python3 scripts/ielts_flow.py init '{"test_number": 7}'
python3 scripts/ielts_flow.py process /path/to/audio.wav
```

---

## Roadmap

| Timeline | Features |
|----------|----------|
| 2026 Q2 | WeChat, Feishu, Enterprise WeChat |
| 2026 Q3 | Hermes Agent, Multi-agent |
| 2026 Q4 | Model fine-tuning, Student dashboard |

---

## Links

- GitHub：https://github.com/KaichenCurry/ielts-speaking-ai
- Question Bank：https://www.notion.so/bba82871-4fe1-4409-9f70-72f6bf27e7b3
- Homework：https://www.notion.so/3412e55d-7136-8179-9ac8-ee60a420ac21
- Error Cases：https://www.notion.so/3412e55d-7136-8113-aa98-cfd36af9799c

---

**Curry Chen** | [GitHub](https://github.com/KaichenCurry)

<p align="center"><strong>⭐ Star this project!</strong></p>
