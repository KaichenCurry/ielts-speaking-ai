# 🎓 ielts-speaking-ai
# 雅思口语 AI 助教系统

> 帮老师自动评分，让老师专注教学。

[![Stars](https://img.shields.io/github/stars/KaichenCurry/ielts-speaking-ai?style=flat-square)](https://github.com/KaichenCurry/ielts-speaking-ai/stargazers)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)](https://www.python.org/)
[![Last Commit](https://img.shields.io/github/last-commit/KaichenCurry/ielts-speaking-ai?style=flat-square)](https://github.com/KaichenCurry/ielts-speaking-ai/commits)

🌐 **语言**: 🇨🇳 **中文** | [🇺🇸 English](README_en.md)

---

## 一句话介绍

帮**雅思口语老师**自动评分的 AI 工具。

老师发一条指令，学生在家语音答题，系统自动评分并逐句反馈，结果自动存档到 Notion。

---

## 解决了什么问题

| 之前 | 之后 |
|------|------|
| 老师手动评分，每份作业 3 小时 | AI 自动评分，0 秒 |
| 学生等一天才能收到反馈 | 答题结束立即收到 |
| 数据散落在微信/邮件 | 自动存档到 Notion |

---

## 工作流程（3 步）

```
Step 1: 老师发指令
        ↓
命令：/题目 Test 07

Step 2: 学生答题
        ↓
🎤 语音答题 → AI 自动评分

Step 3: 收到反馈
        ↓
💬 逐句反馈（语法/词汇/时态/逻辑/思路）
📊 Band Score
📋 自动存档 Notion
```

---

## 效果数据

| 指标 | 数值 |
|------|------|
| 老师效率提升 | 80%+ |
| Band 评分误差 | 0.2 |
| 格式正确率 | 98%+ |

> 基于 2026-04 运营数据（20+ 次练习）

---

## 技术架构

| 环节 | 技术 | 为什么选它 |
|------|------|---------|
| 消息入口 | Telegram | 原生支持语音 |
| AI 推理 | MiniMax（OpenClaw） | 中文理解好 |
| 语音转文字 | Whisper | 口语场景最准 |
| 数据存储 | Notion | 老师直接用 |

```
学生语音 → Whisper → MiniMax → 评分 → Notion
```

---

## 5 大功能

### 1️⃣ 布置作业
一条指令发送 Part 1/2/3 全部题目，66 套真题库

### 2️⃣ AI 自动评分
5 维度逐句反馈：语法 / 词汇 / 时态 / 逻辑 / 思路

### 3️⃣ 即时反馈
答题结束立即收到结果，不用等

### 4️⃣ Notion 存档
学生历史成绩永久留存，随时可查

### 5️⃣ 周报推送
每周五自动推送班级全景报告

---

## 真实案例

**学生回答**：
> "I've been a catering story books for fun... It's a total problem of horizons"

**AI 反馈**：
| 问题 | 诊断 |
|------|------|
| "catering story books" | 词汇错误 → "reading story books" |
| "total problem of horizons" | Chinglish → "broadened my horizons" |

**Band Score**：6.0 / 9.0

---

## 项目结构

```
ielts-speaking-ai/
├── scripts/                    # 核心代码
│   ├── ielts_flow.py         # 主控制器
│   ├── answer_flow.py         # 状态机
│   ├── analyze_transcript.py # AI 评分
│   └── rag_retrieve.py       # RAG 检索
├── docs/
│   ├── SYSTEM_DESIGN.md      # 技术文档
│   └── PORTFOLIO_RESUME.md   # 简历内容
└── references/
    └── prompts.md            # Prompt 模板
```

---

## 快速开始

```bash
# 1. 克隆
git clone https://github.com/KaichenCurry/ielts-speaking-ai.git
cd ielts-speaking-ai

# 2. 安装
pip install -r requirements.txt

# 3. 配置
cp .env.example .env
# 编辑填入 Token

# 4. 运行
python3 scripts/ielts_flow.py init '{"test_number": 7}'
python3 scripts/ielts_flow.py process /path/to/audio.wav
```

---

## 未来功能

| 时间 | 功能 |
|------|------|
| 2026 Q2 | 微信、飞书、企业微信接入 |
| 2026 Q3 | Hermes Agent、多模型编排 |
| 2026 Q4 | 模型微调、学生进度面板 |

---

## 链接

- GitHub：https://github.com/KaichenCurry/ielts-speaking-ai
- 题库：https://www.notion.so/bba82871-4fe1-4409-9f70-72f6bf27e7b3
- 作业库：https://www.notion.so/3412e55d-7136-8179-9ac8-ee60a420ac21
- 错题本：https://www.notion.so/3412e55d-7136-8113-aa98-cfd36af9799c

---

**Curry Chen** | [GitHub](https://github.com/KaichenCurry)

<p align="center"><strong>⭐ Star 这个项目！</strong></p>
