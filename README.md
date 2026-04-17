# 🎓 ielts-speaking-ai

<div align="center">

[![Stars](https://img.shields.io/github/stars/KaichenCurry/ielts-speaking-ai?style=flat-square)](https://github.com/KaichenCurry/ielts-speaking-ai/stargazers)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)](https://www.python.org/)
[![Last Commit](https://img.shields.io/github/last-commit/KaichenCurry/ielts-speaking-ai?style=flat-square)](https://github.com/KaichenCurry/ielts-speaking-ai/commits)

**雅思口语 AI 助教系统 — 帮老师自动评分，让学生即时收到反馈**

[English](./README_en.md) · [项目文档](./docs/SYSTEM_DESIGN.md) · [简历内容](./docs/PORTFOLIO_RESUME.md)

</div>

---

## 🎯 是什么

面向**雅思口语教师**的 AI 助教系统。

老师发一条指令 → 学生在家语音答题 → AI 自动评分 + 逐句反馈 → 结果自动存档 Notion → 周五推送班级周报。

**一句话：把老师从重复性评分工作中解放出来。**

---

## ⚡ 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/KaichenCurry/ielts-speaking-ai.git
cd ielts-speaking-ai

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env，填入 Token

# 4. 运行
python3 scripts/ielts_flow.py init '{"test_number": 7}'
python3 scripts/ielts_flow.py process /path/to/audio.wav
```

---

## 🔄 工作流程

```mermaid
flowchart TD
    subgraph 老师
        A["发送 /题目 Test 07"]
    end

    subgraph 学生
        B["收到题目"]
        C["语音答题"]
        D["收到反馈"]
    end

    subgraph AI系统
        E["Whisper 转写"]
        F["RAG 检索"]
        G["MiniMax 评分"]
    end

    subgraph 数据
        H["Notion 存档"]
    end

    A --> B
    C --> E --> F --> G
    G --> D
    G --> H

    style 老师 fill:#e3f2fd
    style 学生 fill:#f3e5f5
    style AI系统 fill:#fff8e1
    style 数据 fill:#e8f5e9
```

---

## ✨ 核心功能

### 📝 一键布置作业

老师发送一条指令，系统自动发送 Part 1/2/3 全部题目：

```
/题目 Test 07

✅ Part 1 已发送（5题）
✅ Part 2 已发送（Cue Card）
✅ Part 3 已发送（5题）
```

### 🤖 AI 自动评分

| 环节 | 技术 | 说明 |
|------|------|------|
| 语音转文字 | Whisper | OpenAI 开源，口语场景最准 |
| 上下文增强 | RAG | 检索历史错题，让评分更有针对性 |
| AI 评分 | MiniMax | 5 维度逐句反馈 |

### 📊 5 维度逐句反馈

| 维度 | 关注点 | 示例 |
|------|--------|------|
| 语法 | 主谓一致、从句 | "He go" → "He goes" |
| 词汇 | Chinglish、高分词 | "很贵" → "expensive" |
| 时态 | 过去/现在/完成时 | 过去经历用现在时 |
| 逻辑 | 因果、转折 | 观点与举例不匹配 |
| 思路 | 举例、深度 | 举例泛泛而谈 |

### 💾 Notion 自动存档

每个学生的练习记录永久留存：
- 答题原文
- Band Score
- 逐句反馈
- 老师纠正记录

📎 [题库](https://www.notion.so/bba82871-4fe1-4409-9f70-72f6bf27e7b3) · 📎 [作业库](https://www.notion.so/3412e55d-7136-8179-9ac8-ee60a420ac21) · 📎 [错题本](https://www.notion.so/3412e55d-7136-8113-aa98-cfd36af9799c)

### 📈 周报自动推送

每周五 18:00 自动推送到 Telegram 群，包含：
- 练习人次、平均 Band
- Band 分布
- 常见错误 TOP5
- 下周教学建议

---

## 📖 真实案例

**学生回答**：
> "reading has been my hobby since I was a child and I've been a catering story books for fun, but now I'm preparing for my studies abroad and shifted to reading academic articles... It's a total problem of horizons."

**AI 反馈**：

| 原句 | 诊断 | 建议 |
|------|------|------|
| "reading has been my hobby since I was a child" | ✅ 时态正确 | — |
| "I've been a catering story books" | ❌ 词汇：`catering` → `reading` | reading story books |
| "It's a total problem of horizons" | ❌ Chinglish | broadened my horizons |

**Band Score**：6.0 / 9.0

---

## 🛠️ 技术栈

| 环节 | 技术 | 为什么选它 |
|------|------|---------|
| 消息入口 | Telegram | 原生支持语音，跨平台，学生无门槛 |
| AI 推理 | MiniMax（OpenClaw） | 中文理解强，成本低 |
| 语音转文字 | Whisper | 口语场景 SOTA，开源可本地运行 |
| 数据存储 | Notion | 老师直接用，无需自建后台 |

**Band 公式**：
```
综合 Band = Part1×30% + (Part2×40% + Part3×60%)×70%
```

---

## 📁 项目结构

```
ielts-speaking-ai/
├── README.md                     # 本文件
├── README_en.md                 # English version
├── LICENSE                      # MIT
├── requirements.txt             # Python 依赖
├── .env.example                # 环境变量模板
│
├── scripts/                     # 核心代码
│   ├── ielts_flow.py          # 主控制器
│   ├── answer_flow.py          # 状态机（Part1→2→3）
│   ├── analyze_transcript.py  # AI 评分
│   ├── rag_retrieve.py        # RAG 检索
│   ├── notion_append_homework.py
│   ├── notion_append_badcase.py
│   ├── notion_search.py
│   └── weekly_report.py
│
├── docs/                       # 文档
│   ├── SYSTEM_DESIGN.md       # 详细技术文档
│   ├── PORTFOLIO_RESUME.md    # 简历内容
│   └── INTERVIEW_PREP.md      # 面试准备
│
└── references/                # 参考资料
    ├── prompts.md
    └── prompt_changelog.md
```

---

## 🗺️ 未来路线图

```
现在 (v1.0) ─────────────────────────────────────────────────────

    └── 微信 / 飞书 / 企业微信 接入
            │
            ▼
    v1.1 (2026 Q2) ───────────────────────────────────────────

            └── Hermes Agent / 多模型编排 / 向量 RAG
                        │
                        ▼
                v1.2 (2026 Q3) ───────────────────────────────

                            └── 模型微调 / 学生进度面板
                                    │
                                    ▼
                            v2.0 (2026 Q4) ────────────────
```

---

## 📊 效果数据

| 指标 | 目标 | 实际 |
|------|------|------|
| 老师效率提升 | 80%+ | ✅ |
| Band 评分误差 | ≤0.3 | **0.2** |
| 格式正确率 | ≥98% | **98%+** |

> 基于 2026-04 运营数据（20+ 次练习）

---

## 🔗 链接

| 资源 | 地址 |
|------|------|
| GitHub | https://github.com/KaichenCurry/ielts-speaking-ai |
| 题库 | https://www.notion.so/bba82871-4fe1-4409-9f70-72f6bf27e7b3 |
| 作业库 | https://www.notion.so/3412e55d-7136-8179-9ac8-ee60a420ac21 |
| 错题本 | https://www.notion.so/3412e55d-7136-8113-aa98-cfd36af9799c |

---

<div align="center">

**给个 ⭐ 支持一下！**

*Made by [Curry Chen](https://github.com/KaichenCurry)*

</div>
