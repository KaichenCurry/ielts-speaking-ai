# ielts-speaking-ai
# 雅思口语 AI 助教系统

> 面向雅思口语教师的 AI 辅助教学工具 —— 课后作业布置、AI 自动评测、逐句反馈、数据存档、周报分析，让老师专注于真正的教学干预。

🇨🇳 [中文介绍](#中文介绍) | [English](#english)

---

## 🎯 一句话介绍

**雅思口语教师的 AI 助教**：老师一条指令布置作业，学生在家语音答题，系统自动完成评分、逐句反馈、Notion 存档、周报推送，全部无需老师介入。

---

## 👨‍🏫 目标用户

| 用户 | 使用场景 |
|------|---------|
| **雅思口语教师** | 布置作业、查看学生表现、掌握班级进度 |
| **雅思备考学生** | 接收作业、语音答题、收到逐句反馈 |

---

## 💡 核心价值

### 老师的四大痛点，我们一一解决

| 痛点 | 现状 | 解决方案 |
|------|------|---------|
| 重复性评分工作繁重 | 每次作业手动批改 | AI 自动评分，减少 **80%+** 重复工作量 |
| 反馈慢，学生错失记忆窗口 | 次日甚至更久才能收到反馈 | 即时逐句反馈，答题结束立即收到 |
| 学生数据散落，难以追踪 | 无法形成系统化教学档案 | Notion 存档，永久留存，随时可查 |
| 难以批量管理班级进度 | 手动统计费时费力 | 周报自动推送，周五早上 2 分钟看完班级全景 |

---

## 🚀 五大核心功能

### 功能 1️⃣：一键布置作业

**老师操作**：
```
/题目 Test 07
```

**系统自动完成**：
- ✅ Part 1 已发送（5题）
- ✅ Part 2 已发送（Cue Card）
- ✅ Part 3 已发送（5题）

### 功能 2️⃣：AI 自动评测

**技术链路**：
```
学生语音 → Whisper 转写 → RAG 检索历史错题 → MiniMax 5维度评分 → Band Score 计算
```

| AI 环节 | 技术选型 | 作用 |
|---------|---------|------|
| 语音识别 | Whisper | 学生语音 → 文字，无时间限制 |
| 上下文增强 | RAG | 融合 Notion 历史错题，提升评分准确性 |
| 评分推理 | MiniMax | 5 维度精细化评分 |

### 功能 3️⃣：逐句多维度反馈

**Band Score 计算公式**（所有文件统一）：
```
综合 Band = Part1×30% + (Part2×40% + Part3×60%)×70%
```

### 功能 4️⃣：Notion 数据存档

📎 **Notion 数据库链接**（需登录）：
- [题库](https://www.notion.so/bba82871-4fe1-4409-9f70-72f6bf27e7b3) - 66 套真题
- [作业反馈库](https://www.notion.so/3412e55d-7136-8179-9ac8-ee60a420ac21) - 练习存档
- [错题本](https://www.notion.so/3412e55d-7136-8113-aa98-cfd36af9799c) - 错误案例

### 功能 5️⃣：班级周报推送

每周五 18:00 自动推送到 Telegram 群

---

## 📊 效果指标（可信度说明）

| 指标 | 数值 | 评估方法 | 样本量 | 限制说明 |
|------|------|---------|--------|---------|
| Band 评分误差 | **≤0.3** | AI Band 与老师最终确认 Band 的绝对差值 | 2026-04 累计 20+ 次练习 | 样本量有限，分布在 5.0-7.0 分段 |
| 格式正确率 | **98%+** | 每周抽样 10 条检测输出格式一致性 | 连续 4 周监控 | 当前数据来源于 Curry 老师班级 |

> ⚠️ **数据说明**：以上指标基于当前运营数据（2026-04），样本量有限，随着数据积累会持续更新。指标用于内部迭代参考，不代表模型在所有场景下的表现。

---

## 📁 项目结构

```
ielts-speaking-ai/
├── README.md                    # 项目介绍（本文件）
├── SKILL.md                     # 完整系统设计文档
├── .env.example                # 环境变量配置模板
├── requirements.txt            # Python 依赖
│
├── docs/
│   ├── SYSTEM_DESIGN.md        # 详细技术文档
│   └── PORTFOLIO_RESUME.md     # 简历 & 作品集
│
├── scripts/                    # 核心脚本
│   ├── ielts_flow.py          # ⭐ 主流程控制器（Whisper+MiniMax+RAG）
│   ├── answer_flow.py          # ⭐ 状态机实现
│   ├── analyze_transcript.py   # ⭐ AI 评分分析
│   ├── rag_retrieve.py         # ⭐ RAG 检索增强
│   │
│   ├── notion_search.py        # Notion 题库搜索
│   ├── notion_append_homework.py # 作业写入
│   ├── notion_append_badcase.py  # 错题本写入
│   │
│   ├── topic_updater.py        # 题库每周自动更新
│   ├── weekly_report.py        # 周报生成
│   └── evaluate_weekly.py       # 每周效果评估
│
└── references/
    ├── prompts.md              # 评分 Prompt 模板
    └── prompt_changelog.md     # Prompt 迭代日志
```

---

## 🖥️ 快速部署

### 1. 克隆项目

```bash
git clone https://github.com/KaichenCurry/ielts-speaking-ai.git
cd ielts-speaking-ai
```

### 2. 配置环境变量

```bash
# 复制配置模板
cp .env.example .env

# 编辑 .env，填写实际值
nano .env
```

`.env.example` 内容：
```bash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
MINIMAX_API_KEY=your_minimax_api_key_here
NOTION_TOKEN=your_notion_integration_token_here
NOTION_QUESTION_DB_ID=your_question_database_id_here
NOTION_HOMEWORK_DB_ID=your_homework_database_id_here
NOTION_BADCASE_DB_ID=your_badcase_database_id_here
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 运行

```bash
# 初始化会话（示例）
python3 scripts/ielts_flow.py init '{"test_number": 7, "Part 1": ["Q1", "Q2"], "Part 2 题卡": "Describe a shopping mall", "Part 3": ["Q1", "Q2"]}'

# 处理学生音频（自动转写+评分）
python3 scripts/ielts_flow.py process /path/to/audio.wav
```

---

## 📖 真实 Demo 示例

### Demo 1：学生答题与 AI 评分

**学生原音转写**：
> "Definitely, yes, reading has been my hobby since I was a child and I've been a catering story books for fun, but now I'm preparing for my studies abroad and shifted to reading academic articles and biographies of influential figures. It's a total problem of horizons and improve my vocabulary."

**AI 逐句反馈**：

| 原句 | 维度 | 诊断 | 建议 |
|------|------|------|------|
| "reading has been my hobby since I was a child" | ✅ 时态 | 表达自然 | — |
| "I've been a catering story books for fun" | ❌ 词汇 | "catering" 词性误用 | → "reading story books for fun" |
| "shifted to reading academic articles" | ✅ 词汇 | "shifted to" 使用准确 | — |
| "It's a total problem of horizons" | ❌ 词汇 | Chinglish | → "It's really broadened my horizons" |

**评分结果**：
```
Part 1 均分：6.0
Band Score：6.0 / 9.0
```

### Demo 2：完整周报样例

```
📊 班级周报 | 2026.04.11-04.15

═══════════════════════════════════════
【本周练习概览】
═══════════════════════════════════════
• 练习人次：12
• 平均 Band：6.2
• 较上周变化：+0.3 ↑

═══════════════════════════════════════
【Band 分布】
═══════════════════════════════════════
• 7.0+：3人
• 6.0-6.5：6人
• 5.5-6.0：2人

═══════════════════════════════════════
【常见错误 TOP5】
═══════════════════════════════════════
1. 时态混用（过去时 vs 现在时）—— 8次
2. 主谓不一致 —— 6次
3. 举例与观点不匹配 —— 5次

═══════════════════════════════════════
【下周教学建议】
═══════════════════════════════════════
• 重点关注时态一致性训练
• 加强举例具体化引导
```

---

## 🧠 AI 能力设计

### 多模型协同架构

| 环节 | 技术选型 | 代码实现 | 作用 |
|------|---------|---------|------|
| 语音识别 | Whisper | `transcribe_with_whisper()` | 学生语音 → 文字 |
| RAG 检索 | 关键词检索 | `rag_retrieve.py` | 融合历史错题 |
| 评分推理 | MiniMax | `analyze_with_minimax()` | 5 维度评分 |
| Band 计算 | 统一公式 | `calculate_band()` | 综合评分 |

> **代码一致性**：README 中描述的 Whisper + MiniMax + RAG 链路在 `ielts_flow.py` 的 `process` 命令中完整实现（见 `process_answer` 函数）。

### Band Score 计算公式

```python
def calculate_band(p1_avg, p2_score, p3_avg):
    """
    综合 Band = Part1×30% + (Part2×40% + Part3×60%)×70%
    
    示例：
        Part1=6.0, Part2=6.5, Part3=6.0
        Part2_3 = 6.5×0.4 + 6.0×0.6 = 6.2
        Overall = 6.0×0.3 + 6.2×0.7 = 6.14 ≈ 6.0
    """
    p2_3_combined = p2_score * 0.4 + p3_avg * 0.6
    overall = p1_avg * 0.3 + p2_3_combined * 0.7
    return round(overall, 1)
```

此公式在以下文件中保持一致：
- `ielts_flow.py` - 主控制器
- `answer_flow.py` - 状态机
- `weekly_report.py` - 周报生成

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

## 🇨🇳 中文介绍

### 雅思口语 AI 助教系统

面向雅思口语教师的 AI 辅助教学工具，帮助老师：

- **一键布置作业**：66 套真题，随时调用
- **AI 自动评测**：Whisper + MiniMax + RAG，逐句多维度反馈
- **Notion 存档**：学生数据永久留存，支持追踪分析
- **周报推送**：每周五自动推送班级全景报告
- **题库更新**：每周三、六定时自动更新

### 技术亮点

- 多模型协同（Whisper + MiniMax + RAG）
- 三段式状态机（Part 1→Part 2→Part 3）
- Band 评分误差 ≤0.3
- 数据飞轮设计，持续自我进化

---

<p align="center">
  <strong>如果你觉得这个项目有帮助，欢迎点个 ⭐ Star！</strong>
</p>
