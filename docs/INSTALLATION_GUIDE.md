# 📦 IELTS Speaking AI Bot 安装指南

> 面向雅思口语老师的 AI 助教系统。让新手也能快速搭建属于自己的智能助教。

---

## 🎯 这是什么

一个基于 **OpenClaw Agent Framework** 的雅思口语 AI 助教。

**你能用它做什么？**
- ✅ 一键布置作业（Part 1/2/3 全部题目自动发送）
- ✅ 学生语音答题 → AI 自动评分 + 逐句反馈
- ✅ 练习记录自动存档 Notion
- ✅ 每周五自动生成学情周报发送到群

---

## 🧭 路线图

| 步骤 | 你要做什么 | 大概时间 |
|------|-----------|---------|
| 1 | 准备账号 | 5 分钟 |
| 2 | 安装 OpenClaw | 10 分钟 |
| 3 | 配置 Skills | 5 分钟 |
| 4 | 配置 Telegram Bot | 10 分钟 |
| 5 | 连接 Notion | 5 分钟 |
| 6 | 测试运行 | 5 分钟 |

**总计：约 40 分钟完成！**

---

## 📋 第一步：准备账号

你需要准备以下账号：

### 必需

| 服务 | 为什么需要 | 注册地址 |
|------|-----------|---------|
| **Node.js** | OpenClaw 运行环境 | [nodejs.org](https://nodejs.org/) |
| **Telegram Bot** | 消息入口 | [@BotFather](https://t.me/BotFather) |
| **Notion** | 数据存储 | [notion.so](https://www.notion.so/) |

### 可选（后续可加）

| 服务 | 用途 |
|------|------|
| **OpenAI API** | AI 评分引擎 |
| **MiniMax API** | 备用 AI 引擎 |

---

## 🔧 第二步：安装 OpenClaw

### 1. 检查 Node.js

打开终端（Mac 按 `Command + Space`，搜索"终端"）：

```bash
node --version
npm --version
```

如果显示版本号（如 `v20.0.0`），说明已安装。

**如果没有安装**：去 [nodejs.org](https://nodejs.org/) 下载安装。

### 2. 安装 OpenClaw

```bash
npm install -g openclaw
```

### 3. 验证安装

```bash
openclaw --version
```

看到版本号即安装成功。

---

## ⚙️ 第三步：配置 Skills

### 1. 克隆项目

```bash
git clone https://github.com/KaichenCurry/ielts-speaking-ai.git
cd ielts-speaking-ai
```

### 2. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp .env.example .env
nano .env   # 或用任意文本编辑器打开 .env
```

填写以下信息：

```env
# Telegram Bot Token（从 @BotFather 获取）
TELEGRAM_BOT_TOKEN=你的BotToken

# OpenAI API Key（用于 AI 评分）
OPENAI_API_KEY=你的APIKey

# Notion（创建 Integration 后获取）
NOTION_TOKEN=你的NotionToken
```

### 4. 启用 Skills

```bash
openclaw skills init
```

确认看到以下 4 个 Skills：
- ✅ `ielts-speaking` - 主流程
- ✅ `ielts-admin` - 系统管理
- ✅ `ielts-memory` - 记忆管理
- ✅ `ielts-weekly-report` - 智能周报

---

## 📱 第四步：配置 Telegram Bot

### 1. 创建 Bot

1. 在 Telegram 搜索 **@BotFather**
2. 发送 `/newbot`
3. 给 Bot 起名字（如 `雅思口语助教`）
4. 给 Bot 取用户名（必须以 `bot` 结尾，如 `ielts_ai_bot`）
5. 复制 Bot Token

### 2. 把 Bot 加入群组

1. 创建一个 Telegram 群组
2. 把 Bot 加为管理员
3. 在群组发送 `/start`

### 3. 获取群组 ID

把 Bot 加入群后，访问：
```
https://api.telegram.org/bot你的TOKEN/getUpdates
```

在 JSON 中找到 `"chat":{"id":-100xxxxxx}`，这就是群组 ID。

---

## 📋 第五步：配置 Notion

### 1. 创建 Integration

1. 打开 [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. 点击 **+ New integration**
3. 填写名称（如 `IELTS Bot`）
4. 选择你的 Workspace
5. 复制 **Internal Integration Token**

### 2. 创建数据库

在 Notion 中创建 3 个数据库：

| 数据库名 | 用途 | 必要字段 |
|---------|------|---------|
| 题库 | 存放雅思口语题目 | Title, Part1/2/3 Questions |
| 作业反馈库 | 学生答题记录 | Student, Band, Transcript, Feedback |
| 错题本 | 错误记录 | Error Type, Correction |

### 3. 分享数据库给 Integration

1. 打开每个数据库
2. 点击右上角 **...** → **Add connections**
3. 搜索并添加你的 Integration

---

## 🚀 第六步：测试运行

### 1. 启动 OpenClaw Gateway

```bash
openclaw gateway start
```

### 2. 测试 Bot

在 Telegram 群组发送：

```
/start
```

Bot 应该回复欢迎信息。

### 3. 测试布置作业

发送：

```
/题目 Test 01
```

Bot 应该发送 Part 1/2/3 题目。

---

## ❓ 常见问题

### Q: Bot 不响应消息？

**检查：**
1. Bot 是否在群组中？
2. Bot 是否有管理员权限？
3. Gateway 是否运行中？

### Q: 语音无法识别？

**检查：**
1. 学生的语音消息是否在群组中发送？
2. Whisper API 是否配置正确？

### Q: Notion 没有写入？

**检查：**
1. Integration 是否已添加到数据库？
2. 数据库 ID 是否正确配置？

### Q: AI 评分不准确？

**检查：**
1. API Key 是否有额度？
2. 网络是否能访问 OpenAI/MiniMax？

---

## 🎉 恭喜！

你已经成功搭建了自己的雅思口语 AI 助教！

**下一步建议：**
- 📖 阅读 [系统设计文档](./SYSTEM_DESIGN.md)
- 🔧 自定义 Skills 配置
- 📝 添加更多题目到题库

---

## 📞 获取帮助

| 资源 | 链接 |
|------|------|
| GitHub Issues | [提交问题](https://github.com/KaichenCurry/ielts-speaking-ai/issues) |
| 项目文档 | [SYSTEM_DESIGN.md](./SYSTEM_DESIGN.md) |
| 更新日志 | [GitHub Releases](https://github.com/KaichenCurry/ielts-speaking-ai/releases) |

---

<div align="center">

**有疑问？提 Issue！** 🐛

*Made by [Curry Chen](https://github.com/KaichenCurry)*

</div>
