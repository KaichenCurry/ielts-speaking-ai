# 🎓 ielts-speaking-ai
# 雅思口语 AI 助教系统

> 让老师专注于教学，从重复性评分工作中解放。

[![GitHub stars](https://img.shields.io/github/stars/KaichenCurry/ielts-speaking-ai?style=flat-square)](https://github.com/KaichenCurry/ielts-speaking-ai/stargazers)
[![MIT License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)](https://www.python.org/)
[![Last Commit](https://img.shields.io/github/last-commit/KaichenCurry/ielts-speaking-ai?style=flat-square)](https://github.com/KaichenCurry/ielts-speaking-ai/commits)

🌐 **Language**: [🇬🇧 English](README.md) | 🇨🇳 **中文介绍**

---

## 📋 目录

- [🎯 这是什么？](#-这是什么)
- [😤 痛点问题](#-痛点问题)
- [💡 我们的解决方案](#-我们的解决方案)
- [🏗️ 技术栈](#️-技术栈)
- [✨ 核心功能](#-核心功能)
- [📖 真实 Demo](#-真实-demo)
- [🚀 快速开始](#-快速开始)
- [📁 项目结构](#-项目结构)
- [🗺️ 未来路线图](#️-未来路线图)
- [👤 作者](#-作者)

---

## 🎯 这是什么？

一个专为**雅思口语教师**设计的 AI 驱动口语练习与评测系统。

```
老师发送：  /题目 Test 07
        ↓
系统自动发送 Part 1/2/3 全部题目
        ↓
学生在家语音答题
        ↓
AI 自动评分 → 即时逐句反馈
        ↓
数据存档 Notion + 每周五推送周报
```

**目标用户：雅思口语教师**

---

## 😤 痛点问题

| 痛点 | 现状 | 影响 |
|------|------|------|
| 🔴 重复性评分工作 | 每次作业都要手动批改 | 花数小时评分，而非教学设计 |
| 🔴 反馈严重滞后 | 学生次日甚至更久才收到反馈 | 错失最佳记忆窗口 |
| 🔴 数据散落丢失 | 学生记录难以追踪 | 无法形成系统化教学档案 |
| 🔴 班级进度黑盒 | 手动统计费时费力 | 难以针对性调整教学策略 |

---

## 💡 我们的解决方案

### 前后对比

```
┌─────────────────────────────────────────────────────────────────┐
│                        之前（纯人工）                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  老师："批改 20 份作业"                                          │
│       ↓                                                          │
│  ⏱️ 3 小时的重复性评分工作                                        │
│       ↓                                                          │
│  学生："什么时候能收到反馈？"                                      │
│       ↓                                                          │
│  📝 纸质散落，无数据，无追踪                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

                              ↓ ielts-speaking-ai ↓

┌─────────────────────────────────────────────────────────────────┐
│                        之后（AI 驱动）                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  老师："/题目 Test 07"  ← 一条指令                               │
│       ↓                                                          │
│  ✅ 系统自动发送题目                                               │
│       ↓                                                          │
│  学生：语音答题 → 立即收到反馈                                    │
│       ↓                                                          │
│  📊 Notion 存档 + 周五自动推送周报                                │
│       ↓                                                          │
│  老师：专注于真正的教学干预                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ 技术栈

> **为什么选择这三者？它们共同构成了完美的 AI 助教组合。**

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│   📱 Telegram          +   🤖 OpenClaw          +   📋 Notion   │
│   ──────────────           ─────────────           ───────────  │
│                                                                  │
│   🌐 即时通讯              🧠 AI Agent 核心        📊 数据存储    │
│   原生语音支持             多模型融合              结构化文档      │
│   跨平台支持               原生中文理解             可扩展存档      │
│   低门槛                  成熟平台                教师友好        │
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  🎤 语音 → 📝 Whisper → 🧠 MiniMax → 📊 Band 评分   │   │
│   │              ↑ OpenClaw Agent 编排 ↑                   │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 为什么要用 Telegram？

| 优势 | 说明 |
|------|------|
| 🌐 原生语音支持 | Telegram 原生支持语音消息，完美适配口语练习 |
| 🌍 多语言环境 | 内置翻译功能，国际学生也能用 |
| 📱 跨平台 | iOS/Android/Desktop，学生随时随地练习 |
| 🔔 即时通知 | 学生立即收到题目 |
| 📊 群组功能 | 内置群报告，周报推送 |

### 为什么要用 OpenClaw？

| 优势 | 说明 |
|------|------|
| 🧠 成熟的 AI Agent | 原生集成 Whisper + MiniMax + RAG |
| 🔄 工作流自动化 | Part 1→2→3 状态机自动编排 |
| 🌐 中文原生 | 优秀的中文语境理解能力 |
| 💰 成本效益 | 相比 GPT-4，更适合教育场景 |

### 为什么要用 Notion？

| 优势 | 说明 |
|------|------|
| 📊 结构化数据 | 题库、作业存档、错题本 |
| 📝 教师友好 | 无代码数据库，非技术老师也能用 |
| 🔗 API 集成 | 自动存档作业，可搜索 |
| 📈 进度追踪 | 学生成长轨迹可视化 |

---

## ✨ 核心功能

### 1️⃣ 一键布置作业
```
/题目 Test 07

✅ Part 1 已发送（5题）
✅ Part 2 已发送（Cue Card）
✅ Part 3 已发送（5题）
```
66 套真题，随时调用。

### 2️⃣ AI 自动评测

| 环节 | 技术选型 | 功能 |
|------|---------|------|
| 🎤 语音转文字 | **Whisper** (OpenAI) | 语音 → 文字 |
| 📚 上下文增强 | **RAG** | 历史错题提升评分准确性 |
| 🧠 评分推理 | **MiniMax** (通过 OpenClaw) | 5 维度精细化评分 |
| 📊 Band 计算 | **公式** | Part1×30% + (Part2×40%+Part3×60%)×70% |

### 3️⃣ 5 维度逐句反馈

| 维度 | 关注点 | 示例问题 |
|------|--------|---------|
| 📝 语法 | 主谓一致、从句、介词 | "He go" → "He goes" |
| 📖 词汇 | Chinglish、高分替换 | "很贵" → "expensive" |
| ⏰ 时态 | 过去/现在/完成时 | 过去经历用现在时 |
| 🔗 逻辑 | 因果、转折、跑题 | 观点与举例不匹配 |
| 💡 思路 | 举例、深度、观点 | 举例泛泛而谈 |

### 4️⃣ Notion 数据存档

📎 **数据库链接**：
- [题库](https://www.notion.so/bba82871-4fe1-4409-9f70-72f6bf27e7b3) - 66 套真题
- [作业反馈库](https://www.notion.so/3412e55d-7136-8179-9ac8-ee60a420ac21) - 练习存档
- [错题本](https://www.notion.so/3412e55d-7136-8113-aa98-cfd36af9799c) - 错误案例

### 5️⃣ 周报自动推送

每周五 18:00 自动推送到 Telegram 群

```
📊 周报 | 2026.04.11-04.15

【练习概览】
• 练习人次：12
• 平均 Band：6.2
• 较上周变化：+0.3 ↑

【Band 分布】
• 7.0+：3人 ████
• 6.0-6.5：6人 ████████████
• 5.5-6.0：2人 ████

【常见错误 TOP5】
1. 时态混用 —— 8次
2. 主谓不一致 —— 6次
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

**评分结果**：Band Score **6.0 / 9.0**

---

## 📊 效果指标

> ⚠️ **可信度说明**：基于 2026-04 运营数据（20+ 次练习），仅供参考。

| 指标 | 目标 | 实际 | 样本量 |
|------|------|------|--------|
| Band 评分误差 | ≤0.3 | **0.2** | 20+ 次 |
| 格式正确率 | ≥98% | **98%+** | 每周抽样 |

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

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填写实际 Token
```

```bash
# 必需的 Token：
TELEGRAM_BOT_TOKEN=your_bot_token      # 找 @BotFather 申请
MINIMAX_API_KEY=your_api_key          # 通过 OpenClaw 网关
NOTION_TOKEN=your_notion_token         # 从 notion.so/my-integrations
NOTION_QUESTION_DB_ID=your_db_id      # 题库数据库 ID
NOTION_HOMEWORK_DB_ID=your_db_id       # 作业反馈库 ID
NOTION_BADCASE_DB_ID=your_db_id       # 错题本 ID
```

### 4. 运行

```bash
# 初始化会话
python3 scripts/ielts_flow.py init '{"test_number": 7, "Part 1": ["Q1", "Q2"], "Part 2 题卡": "Describe a shopping mall", "Part 3": ["Q1", "Q2"]}'

# 处理学生音频（自动转写+评分）
python3 scripts/ielts_flow.py process /path/to/audio.wav
```

---

## 📁 项目结构

```
ielts-speaking-ai/
│
├── 📄 README.md                # 英文版（主）
├── 📄 README_zh.md             # 中文介绍（本文件）
│
├── 🔧 核心脚本
│   ├── ielts_flow.py          # ⭐ 主流程控制器
│   ├── answer_flow.py          # ⭐ 状态机（Part1→2→3）
│   ├── analyze_transcript.py   # ⭐ AI 评分分析
│   └── rag_retrieve.py         # ⭐ RAG 检索
│
├── 📱 平台集成
│   ├── notion_search.py         # Notion 题库
│   ├── notion_append_homework.py # 作业存档
│   └── notion_append_badcase.py  # 错题本
│
├── 🔄 自动化
│   ├── topic_updater.py         # 题库自动更新
│   ├── weekly_report.py          # 周报生成
│   └── evaluate_weekly.py        # 每周评估
│
└── 📚 文档
    ├── docs/SYSTEM_DESIGN.md    # 详细技术文档
    └── docs/PORTFOLIO_RESUME.md # 简历 & 作品集
```

---

## 🗺️ 未来路线图

### 当前版本 ✅
```
┌─────────────────────────────────────────────────────┐
│                   当前版本: v1.0                    │
├─────────────────────────────────────────────────────┤
│                                                      │
│  📱 Telegram Bot                                     │
│  🤖 OpenClaw Agent (MiniMax + Whisper)              │
│  📋 Notion Integration                              │
│                                                      │
│  ✅ 语音练习                                         │
│  ✅ AI 自动评分                                      │
│  ✅ 逐句多维度反馈                                   │
│  ✅ Notion 数据存档                                  │
│  ✅ 周报自动推送                                     │
│  ✅ 66 套真题题库                                   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### 未来版本 🔜

```
┌─────────────────────────────────────────────────────┐
│                   未来路线图                         │
├─────────────────────────────────────────────────────┤
│                                                      │
│  v1.1 (2026 Q2)                                    │
│  ├── 🔜 微信小程序集成                               │
│  ├── 🔜 飞书/Lark Bot 集成                          │
│  └── 🔜 企业微信集成                                 │
│                                                      │
│  v1.2 (2026 Q3)                                    │
│  ├── 🔜 Hermes Agent (OpenClaw 下一代)              │
│  ├── 🔜 多 Agent 编排                               │
│  └── 🔜 向量检索升级 RAG                            │
│                                                      │
│  v2.0 (2026 Q4)                                    │
│  ├── 🔜 飞书文档集成                                 │
│  ├── 🔜 腾讯文档集成                                 │
│  ├── 🔜 基于积累数据的模型微调                       │
│  └── 🔜 学生进度可视化面板                          │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### 为什么要扩展到微信/飞书？

| 平台 | 对本项目的优势 |
|------|--------------|
| 💬 **微信** | 12 亿+ 用户，国内绝对主导，学生已有微信 |
| 📱 **飞书/Lark** | 企业/教育场景优秀，内置日历和协作 |
| 🏢 **企业微信** | 已有企业微信的语言学校可直接接入 |
| 📄 **飞书/腾讯文档** | 已用这些工具的团队可直接替换 Notion |

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

| 平台 | 链接 |
|------|------|
| 🌐 GitHub | [@KaichenCurry](https://github.com/KaichenCurry) |
| 📂 项目 | https://github.com/KaichenCurry/ielts-speaking-ai |

---

## 📜 License

MIT License - 详见 [LICENSE](LICENSE) 文件。

---

<p align="center">
  <strong>⭐ 如果这个项目对你有帮助，请点个 Star！</strong>
</p>
