# 🎓 ielts-speaking-ai
# 雅思口语 AI 助教系统

> 让老师专注于教学，从重复性评分工作中解放。

[![Stars](https://img.shields.io/github/stars/KaichenCurry/ielts-speaking-ai?style=flat-square)](https://github.com/KaichenCurry/ielts-speaking-ai/stargazers)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)](https://www.python.org/)
[![Last Commit](https://img.shields.io/github/last-commit/KaichenCurry/ielts-speaking-ai?style=flat-square)](https://github.com/KaichenCurry/ielts-speaking-ai/commits)

🌐 **语言**: 🇨🇳 **中文** | [🇺🇸 English](README_en.md)

---

## 📋 目录

- [🎯 项目介绍](#-项目介绍)
- [😤 痛点问题](#-痛点问题)
- [💡 解决方案](#-解决方案)
- [🏗️ 技术架构](#️-技术架构)
- [✨ 核心功能](#-核心功能)
- [📖 真实 Demo](#-真实-demo)
- [📁 项目结构](#-项目结构)
- [🗺️ 未来路线图](#️-未来路线图)
- [🚀 快速开始](#-快速开始)

---

## 🎯 项目介绍

### 一句话

面向**雅思口语教师**的 AI 助教系统，老师一条指令布置作业，学生在家语音答题，系统自动完成评分、逐句反馈、Notion 存档、周报推送。

### 解决什么问题

| 用户 | 痛点 | 解决方案 |
|------|------|---------|
| 老师 | 重复性评分工作繁重 | AI 自动评分，减少 80%+ 工作量 |
| 老师 | 反馈严重滞后 | 即时逐句反馈，答题结束即收到 |
| 老师 | 学生数据散落 | Notion 存档，随时可查 |
| 老师 | 班级进度黑盒 | 周五自动推送班级全景周报 |

---

## 😤 痛点问题

### 之前 vs 之后

```mermaid
flowchart LR
    subgraph Before["之前（纯人工）"]
        B1["📋 收到20份作业"]
        B2["⏱️ 手动评分 → 3小时"]
        B3["😤 学生问：什么时候反馈？"]
        B4["📝 纸质散落，无数据"]
    end

    B1 --> B2 --> B3 --> B4

    style Before fill:#ffcccc,stroke:#ff6666
```

```mermaid
flowchart LR
    subgraph After["之后（AI驱动）"]
        A1["👨‍🏫 发送 /题目 Test 07"]
        A2["✅ 系统自动发送 Part 1/2/3"]
        A3["🎤 学生语音答题"]
        A4["📊 AI 即时评分 → 💬 逐句反馈"]
        A5["📋 Notion 存档 + 📈 周五周报"]
        A6["👨‍🏫 专注教学干预"]
    end

    A1 --> A2 --> A3 --> A4 --> A5 --> A6

    style After fill:#ccffcc,stroke:#66cc66
```

---

## 💡 解决方案

### 完整工作流

```mermaid
flowchart TD
    subgraph Teacher["👨‍🏫 老师"]
        T1["发送 /题目 Test XX"]
        T2["查看 Notion"]
        T3["接收周五周报"]
    end

    subgraph System["🤖 系统"]
        S1["Telegram Bot"]
        S2["Whisper 语音转写"]
        S3["RAG 历史错题检索"]
        S4["MiniMax AI 评分"]
        S5["Band Score 计算"]
    end

    subgraph Student["🎓 学生"]
        Sd1["接收题目"]
        Sd2["语音答题"]
        Sd3["收到逐句反馈"]
    end

    subgraph Storage["📋 Notion"]
        DB1["题库 66套"]
        DB2["作业反馈库"]
        DB3["错题本"]
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

## 🏗️ 技术架构

### 为什么选这三个平台？

```mermaid
flowchart TD
    subgraph Tech["技术栈"]
        T1["📱 Telegram"]
        T2["🤖 OpenClaw"]
        T3["📋 Notion"]
    end

    subgraph Reason1["为什么 Telegram"]
        R1a["🎤 原生语音支持"]
        R1b["🌍 多语言环境"]
        R1c["📱 跨平台"]
    end

    subgraph Reason2["为什么 OpenClaw"]
        R2a["🧠 AI Agent 核心"]
        R2b["🔄 Workflow 自动编排"]
        R2c["🌐 中文理解强"]
    end

    subgraph Reason3["为什么 Notion"]
        R3a["📊 结构化数据库"]
        R3b["📝 教师友好"]
        R3c["🔗 API 集成"]
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

### AI 流水线

```mermaid
flowchart LR
    A["🎤 语音"] -->|Whisper| B["📝 文字"]
    B -->|RAG| C["🧠 上下文"]
    C -->|MiniMax| D["📊 Band 评分"]
    D -->|Notion| E["💾 存档"]

    style A fill:#e1f5fe,stroke:#03a9f4
    style D fill:#fff8e1,stroke:#ffc107
    style E fill:#e8f5e9,stroke:#4caf50
```

---

## ✨ 核心功能

### 1️⃣ 一键布置作业

```
命令：/题目 Test 07

✅ Part 1 已发送（5题）
✅ Part 2 已发送（Cue Card）
✅ Part 3 已发送（5题）
```

### 2️⃣ AI 自动评测

```mermaid
flowchart LR
    subgraph Pipeline["AI 流水线"]
        P1["🎤 Whisper"] --> P2["📝 文字"]
        P2 --> P3["📚 RAG"]
        P3 --> P4["🧠 MiniMax"]
        P4 --> P5["📊 Band"]
    end

    style P1 fill:#e1f5fe
    style P4 fill:#fff8e1
    style P5 fill:#fff3e0
```

| 环节 | 技术 | 作用 |
|------|------|------|
| 🎤 语音识别 | Whisper | 语音 → 文字 |
| 📚 上下文增强 | RAG | 历史错题检索 |
| 🧠 评分推理 | MiniMax | 5 维度评分 |
| 📊 Band 计算 | 公式 | Part1×30% + (Part2×40%+Part3×60%)×70% |

### 3️⃣ 逐句多维度反馈

| 维度 | 关注点 | 示例 |
|------|--------|------|
| 📝 语法 | 主谓一致、从句 | "He go" → "He goes" |
| 📖 词汇 | Chinglish、高分词 | "很贵" → "expensive" |
| ⏰ 时态 | 过去/现在/完成时 | 过去经历用现在时 |
| 🔗 逻辑 | 因果、转折 | 观点与举例不匹配 |
| 💡 思路 | 举例、深度 | 举例泛泛而谈 |

### 4️⃣ Notion 数据存档

📎 [题库](https://www.notion.so/bba82871-4fe1-4409-9f70-72f6bf27e7b3) | 📎 [作业反馈库](https://www.notion.so/3412e55d-7136-8179-9ac8-ee60a420ac21) | 📎 [错题本](https://www.notion.so/3412e55d-7136-8113-aa98-cfd36af9799c)

### 5️⃣ 周报自动推送

```mermaid
flowchart TD
    W1["⏰ 每周五 18:00"] --> W2["📊 生成周报"]
    W2 --> W3["📱 推送 Telegram"]
    W3 --> W4["👨‍🏫 老师 2 分钟看完"]

    W4 --> W5["练习人次 + Band分布"]
    W4 --> W6["常见错误 TOP5"]
    W4 --> W7["下周教学建议"]

    style W1 fill:#e1f5fe
    style W3 fill:#e8f5e9
```

---

## 📖 真实 Demo

### 学生答题 → AI 反馈

**原音转写**：
> "Definitely, yes, reading has been my hobby since I was a child and I've been a catering story books for fun, but now I'm preparing for my studies abroad and shifted to reading academic articles..."

**AI 逐句反馈**：

| 原句 | 语法 | 词汇 | 时态 | 逻辑 | 思路 |
|------|------|------|------|------|------|
| "reading has been my hobby since I was a child" | ✅ | ✅ | ✅ | ✅ | ✅ |
| "I've been a catering story books" | ✅ | ❌ `catering` → `reading` | ✅ | ✅ | ✅ |
| "shifted to reading academic articles" | ✅ | ✅ | ✅ | ✅ | ✅ |
| "It's a total problem of horizons" | ✅ | ❌ Chinglish → `broadened my horizons` | ✅ | ✅ | ✅ |

**结果**：Band Score **6.0 / 9.0**

---

## 📁 项目结构

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

## 🗺️ 未来路线图

### 技术演进

```mermaid
flowchart LR
    subgraph V1["v1.0（当前）"]
        V1A["📱 Telegram"]
        V1B["🤖 OpenClaw<br/>(MiniMax)"]
        V1C["📚 关键词 RAG"]
        V1D["📋 Notion"]
    end

    subgraph V2["v1.2（Q3）"]
        V2A["📱 Telegram"]
        V2B["🤖 OpenClaw<br/>(Multi-Agent)"]
        V2C["📚 向量 RAG"]
        V2D["📋 Notion"]
    end

    subgraph V3["v2.0（Q4）"]
        V3A["📱 Telegram"]
        V3B["🤖 Hermes Agent"]
        V3C["📚 微调模型"]
        V3D["📋 飞书/腾讯文档"]
    end

    V1 --> V2 --> V3

    style V1 fill:#e8f5e9,stroke:#4caf50
    style V2 fill:#fff8e1,stroke:#ffc107
    style V3 fill:#e3f2fd,stroke:#03a9f4
```

### 版本功能

```mermaid
gantt
    title 未来路线图
    dateFormat  YYYY-MM
    section v1.1
    微信小程序集成       :2026-07, 2026-09
    飞书/Lark Bot       :2026-07, 2026-09
    企业微信集成         :2026-07, 2026-09
    section v1.2
    Hermes Agent        :2026-10, 2026-12
    多 Agent 编排       :2026-10, 2026-12
    向量检索升级 RAG    :2026-10, 2026-12
    section v2.0
    飞书文档集成        :2027-01, 2027-03
    腾讯文档集成        :2027-01, 2027-03
    模型微调            :2027-01, 2027-03
    学生进度面板        :2027-01, 2027-03
```

---

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/KaichenCurry/ielts-speaking-ai.git
cd ielts-speaking-ai
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境
```bash
cp .env.example .env
# 编辑 .env 填写 Token
```

### 4. 运行
```bash
python3 scripts/ielts_flow.py init '{"test_number": 7}'
python3 scripts/ielts_flow.py process /path/to/audio.wav
```

---

## 📊 效果指标

> ⚠️ **可信度说明**：基于 2026-04 运营数据（20+ 次练习），仅供参考。

| 指标 | 目标 | 实际 |
|------|------|------|
| Band 评分误差 | ≤0.3 | **0.2** |
| 格式正确率 | ≥98% | **98%+** |

---

## 🔄 数据飞轮

```mermaid
flowchart LR
    F1["🎓 学生答题"] --> F2["📊 AI 评分"]
    F2 --> F3["👨‍🏫 老师纠正"]
    F3 --> F4["📚 错题本收录"]
    F4 --> F5["📚 RAG 增强"]
    F5 --> F2

    F4 -.->|"100+条后"| F6["🔧 模型微调"]
    F6 --> F2

    style F1 fill:#e1f5fe
    style F2 fill:#fff8e1
    style F3 fill:#f3e5f5
    style F4 fill:#e8f5e9
    style F5 fill:#e8f5e9
```

---

## 👤 作者

**Curry Chen** | [GitHub](https://github.com/KaichenCurry) | [项目链接](https://github.com/KaichenCurry/ielts-speaking-ai)

---

## 📜 License

[MIT License](LICENSE)

---

<p align="center">
  <strong>⭐ Star this project if you find it helpful!</strong>
</p>
