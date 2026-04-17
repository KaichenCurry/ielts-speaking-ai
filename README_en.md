# 🎓 ielts-speaking-ai
# IELTS Speaking AI Assistant

> Free teachers from repetitive grading, let them focus on real teaching.

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
- [📁 Structure](#-structure)
- [🗺️ Roadmap](#️-roadmap)
- [🚀 Quick Start](#-quick-start)

---

## 🎯 What is this?

### One-sentence

An AI-powered assistant for **IELTS speaking teachers** — one command to assign homework, students practice with voice, system auto-grades, provides sentence-by-sentence feedback, archives to Notion, and pushes weekly reports.

### What Problem It Solves

| User | Problem | Solution |
|------|---------|----------|
| Teachers | Repetitive grading | AI auto-grades, 80%+ time saved |
| Teachers | Delayed feedback | Instant feedback after practice |
| Teachers | Scattered data | Notion archives, searchable |
| Teachers | No class overview | Auto Friday weekly reports |

---

## 😤 The Problem

### Before vs After

```mermaid
flowchart LR
    subgraph Before["BEFORE (Manual)"]
        B1["📋 Receive 20 assignments"]
        B2["⏱️ Manual grading → 3 hours"]
        B3["😤 Student: When feedback?"]
        B4["📝 Papers scattered, no data"]
    end

    B1 --> B2 --> B3 --> B4

    style Before fill:#ffcccc,stroke:#ff6666
```

```mermaid
flowchart LR
    subgraph After["AFTER (AI-Powered)"]
        A1["👨‍🏫 Send /题目 Test 07"]
        A2["✅ Auto send Part 1/2/3"]
        A3["🎤 Student voice practice"]
        A4["📊 AI instant grading → 💬 Feedback"]
        A5["📋 Notion archive + 📈 Friday report"]
        A6["👨‍🏫 Focus on teaching"]
    end

    A1 --> A2 --> A3 --> A4 --> A5 --> A6

    style After fill:#ccffcc,stroke:#66cc66
```

---

## 💡 Our Solution

### Complete Workflow

```mermaid
flowchart TD
    subgraph Teacher["👨‍🏫 Teacher"]
        T1["Send /题目 Test XX"]
        T2["Check Notion"]
        T3["Receive Friday report"]
    end

    subgraph System["🤖 System"]
        S1["Telegram Bot"]
        S2["Whisper STT"]
        S3["RAG Retrieval"]
        S4["MiniMax Scoring"]
        S5["Band Calculation"]
    end

    subgraph Student["🎓 Student"]
        Sd1["Receive questions"]
        Sd2["Voice practice"]
        Sd3["Get feedback"]
    end

    subgraph Storage["📋 Notion"]
        DB1["Question Bank (66)"]
        DB2["Homework Archive"]
        DB3["Error Cases"]
    end

    T1 --> S1
    S1 --> Sd1
    Sd2 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> Sd3
    S5 --> DB2
    T2 --> DB2
    T2 --> DB3
    T3 --> DB2
    DB2 -.-> DB3

    style Teacher fill:#e3f2fd,stroke:#2196f3
    style System fill:#fff8e1,stroke:#ffc107
    style Student fill:#f3e5f5,stroke:#9c27b0
    style Storage fill:#e8f5e9,stroke:#4caf50
```

---

## 🏗️ Tech Stack

### Why These Three?

```mermaid
flowchart TD
    subgraph Tech["Tech Stack"]
        T1["📱 Telegram"]
        T2["🤖 OpenClaw"]
        T3["📋 Notion"]
    end

    subgraph Reason1["Why Telegram?"]
        R1a["🎤 Native voice support"]
        R1b["🌍 Multi-language"]
        R1c["📱 Cross-platform"]
    end

    subgraph Reason2["Why OpenClaw?"]
        R2a["🧠 AI Agent core"]
        R2b["🔄 Workflow automation"]
        R2c["🌐 Chinese understanding"]
    end

    subgraph Reason3["Why Notion?"]
        R3a["📊 Structured database"]
        R3b["📝 Teacher-friendly"]
        R3c["🔗 API integration"]
    end

    T1 --> R1a
    T1 --> R1b
    T1 --> R1c
    T2 --> R2a
    T2 --> R2b
    T2 --> R2c
    T3 --> R3a
    T3 --> R3b
    T3 --> R3c

    style Tech fill:#e1f5fe,stroke:#03a9f4
    style Reason1 fill:#e3f2fd,stroke:#2196f3
    style Reason2 fill:#fff8e1,stroke:#ffc107
    style Reason3 fill:#e8f5e9,stroke:#4caf50
```

### AI Pipeline

```mermaid
flowchart LR
    A["🎤 Voice"] -->|Whisper| B["📝 Text"]
    B -->|RAG| C["🧠 Context"]
    C -->|MiniMax| D["📊 Band Score"]
    D -->|Notion| E["💾 Archive"]

    style A fill:#e1f5fe,stroke:#03a9f4
    style D fill:#fff8e1,stroke:#ffc107
    style E fill:#e8f5e9,stroke:#4caf50
```

---

## ✨ Features

### 1️⃣ One-Click Assignment
```
Command: /题目 Test 07

✅ Part 1 sent (5 questions)
✅ Part 2 sent (Cue Card)
✅ Part 3 sent (5 questions)
```

### 2️⃣ AI Auto-Scoring

```mermaid
flowchart LR
    subgraph Pipeline["AI Pipeline"]
        P1["🎤 Whisper"] --> P2["📝 Text"]
        P2 --> P3["📚 RAG"]
        P3 --> P4["🧠 MiniMax"]
        P4 --> P5["📊 Band"]
    end

    style P1 fill:#e1f5fe
    style P4 fill:#fff8e1
    style P5 fill:#fff3e0
```

| Component | Technology | Function |
|-----------|------------|----------|
| 🎤 Speech-to-Text | Whisper | Voice → Text |
| 📚 Context | RAG | Historical errors |
| 🧠 Scoring | MiniMax | 5-dimension evaluation |
| 📊 Band Calc | Formula | Part1×30% + (Part2×40%+Part3×60%)×70% |

### 3️⃣ 5-Dimension Feedback

| Dimension | Focus | Example |
|-----------|-------|---------|
| 📝 Grammar | Subject-verb, clauses | "He go" → "He goes" |
| 📖 Vocabulary | Chinglish, synonyms | "很贵" → "expensive" |
| ⏰ Tense | Past/present/perfect | Past events in present |
| 🔗 Logic | Causality, transitions | Example doesn't match point |
| 💡 Ideas | Examples, depth | Examples too general |

### 4️⃣ Notion Integration

📎 [Question Bank](https://www.notion.so/bba82871-4fe1-4409-9f70-72f6bf27e7b3) | 📎 [Homework Archive](https://www.notion.so/3412e55d-7136-8179-9ac8-ee60a420ac21) | 📎 [Error Cases](https://www.notion.so/3412e55d-7136-8113-aa98-cfd36af9799c)

### 5️⃣ Weekly Reports

```mermaid
flowchart TD
    W1["⏰ Every Friday 18:00"] --> W2["📊 Generate report"]
    W2 --> W3["📱 Push to Telegram"]
    W3 --> W4["👨‍🏫 Teacher reads in 2 min"]

    W4 --> W5["Sessions + Band distribution"]
    W4 --> W6["Common errors TOP5"]
    W4 --> W7["Next week suggestions"]

    style W1 fill:#e1f5fe
    style W3 fill:#e8f5e9
```

---

## 📖 Demo

### Student Answer → AI Feedback

**Transcript**:
> "Definitely, yes, reading has been my hobby since I was a child and I've been a catering story books for fun..."

**AI Feedback**:

| Sentence | Grammar | Vocabulary | Tense | Logic | Ideas |
|----------|---------|-----------|-------|-------|-------|
| "reading has been my hobby since I was a child" | ✅ | ✅ | ✅ | ✅ | ✅ |
| "I've been a catering story books" | ✅ | ❌ `catering` → `reading` | ✅ | ✅ | ✅ |
| "shifted to reading academic articles" | ✅ | ✅ | ✅ | ✅ | ✅ |
| "It's a total problem of horizons" | ✅ | ❌ Chinglish → `broadened my horizons` | ✅ | ✅ | ✅ |

**Result**: Band Score **6.0 / 9.0**

---

## 📁 Structure

```mermaid
flowchart TD
    subgraph Root["📁 ielts-speaking-ai"]
        R1["📄 README.md"] 
        R2["📄 README_en.md"]
        R3["📄 LICENSE"]
        R4["📄 .env.example"]
        R5["📄 requirements.txt"]
    end

    subgraph Scripts["📁 scripts/"]
        S1["⭐ ielts_flow.py"]
        S2["⭐ answer_flow.py"]
        S3["⭐ analyze_transcript.py"]
        S4["⭐ rag_retrieve.py"]
        S5["📱 notion_*.py"]
        S6["🔄 weekly_report.py"]
    end

    subgraph Docs["📁 docs/"]
        D1["📋 SYSTEM_DESIGN.md"]
        D2["📋 PORTFOLIO_RESUME.md"]
        D3["📋 INTERVIEW_PREP.md"]
    end

    subgraph Ref["📁 references/"]
        Ref1["📝 prompts.md"]
        Ref2["📝 prompt_changelog.md"]
    end

    Root --> Scripts
    Root --> Docs
    Root --> Ref

    style Root fill:#e1f5fe,stroke:#03a9f4
    style Scripts fill:#fff8e1,stroke:#ffc107
    style Docs fill:#f3e5f5,stroke:#9c27b0
    style Ref fill:#e8f5e9,stroke:#4caf50
```

---

## 🗺️ Roadmap

### Tech Evolution

```mermaid
flowchart LR
    subgraph V1["v1.0 (Current)"]
        V1A["📱 Telegram"]
        V1B["🤖 OpenClaw<br/>(MiniMax)"]
        V1C["📚 Keyword RAG"]
        V1D["📋 Notion"]
    end

    subgraph V2["v1.2 (Q3)"]
        V2A["📱 Telegram"]
        V2B["🤖 OpenClaw<br/>(Multi-Agent)"]
        V2C["📚 Vector RAG"]
        V2D["📋 Notion"]
    end

    subgraph V3["v2.0 (Q4)"]
        V3A["📱 Telegram"]
        V3B["🤖 Hermes Agent"]
        V3C["📚 Fine-tuned Model"]
        V3D["📋 Feishu/Tencent Docs"]
    end

    V1 --> V2 --> V3

    style V1 fill:#e8f5e9,stroke:#4caf50
    style V2 fill:#fff8e1,stroke:#ffc107
    style V3 fill:#e3f2fd,stroke:#03a9f4
```

### Version Timeline

```mermaid
gantt
    title Roadmap
    dateFormat  YYYY-MM
    section v1.1
    WeChat Mini Program       :2026-07, 2026-09
    Feishu/Lark Bot         :2026-07, 2026-09
    Enterprise WeChat         :2026-07, 2026-09
    section v1.2
    Hermes Agent             :2026-10, 2026-12
    Multi-Agent              :2026-10, 2026-12
    Vector RAG               :2026-10, 2026-12
    section v2.0
    Feishu Docs              :2027-01, 2027-03
    Tencent Docs             :2027-01, 2027-03
    Model Fine-tuning         :2027-01, 2027-03
    Student Dashboard        :2027-01, 2027-03
```

---

## 🚀 Quick Start

### 1. Clone
```bash
git clone https://github.com/KaichenCurry/ielts-speaking-ai.git
cd ielts-speaking-ai
```

### 2. Install
```bash
pip install -r requirements.txt
```

### 3. Configure
```bash
cp .env.example .env
# Edit .env with your tokens
```

### 4. Run
```bash
python3 scripts/ielts_flow.py init '{"test_number": 7}'
python3 scripts/ielts_flow.py process /path/to/audio.wav
```

---

## 📊 Metrics

> ⚠️ **Disclaimer**: Based on limited data (20+ sessions, April 2026).

| Metric | Target | Actual |
|--------|--------|--------|
| Band Error | ≤0.3 | **0.2** |
| Format Accuracy | ≥98% | **98%+** |

---

## 🔄 Data Flywheel

```mermaid
flowchart LR
    F1["🎓 Student practice"] --> F2["📊 AI scoring"]
    F2 --> F3["👨‍🏫 Teacher correction"]
    F3 --> F4["📚 Error cases"]
    F4 --> F5["📚 RAG enhancement"]
    F5 --> F2

    F4 -.->|"100+ records"| F6["🔧 Fine-tuning"]
    F6 --> F2

    style F1 fill:#e1f5fe
    style F2 fill:#fff8e1
    style F3 fill:#f3e5f5
    style F4 fill:#e8f5e9
    style F5 fill:#e8f5e9
```

---

## 👤 Author

**Curry Chen** | [GitHub](https://github.com/KaichenCurry) | [Project](https://github.com/KaichenCurry/ielts-speaking-ai)

---

## 📜 License

[MIT License](LICENSE)

---

<p align="center">
  <strong>⭐ Star this project if you find it helpful!</strong>
</p>
