# Gas Town

**基于 Claude Code 的多智能体编排系统，支持持久化工作追踪**

## 概述

Gas Town 是一个工作空间管理器，用于协调多个 Claude Code 智能体处理不同任务。通过 git 支持的钩子系统持久化工作状态，实现可靠的多智能体工作流。

### 解决的问题

| 挑战 | Gas Town 解决方案 |
|------|-------------------|
| 智能体重启后丢失上下文 | 工作状态持久化在 git 支持的钩子中 |
| 手动协调智能体 | 内置邮箱、身份和交接机制 |
| 4-10 个智能体变得混乱 | 可扩展至 20-30 个智能体 |
| 工作状态丢失在智能体内存中 | 工作状态存储在 Beads 账本中 |

## 核心概念

### 市长 (The Mayor) 🎩

您的主要 AI 协调器。市长是一个拥有完整工作空间、项目和智能体上下文的 Claude Code 实例。**从这里开始**——直接告诉市长您想完成什么。

### 小镇 (Town) 🏘️

您的工作空间目录（如 `~/gt/`），包含所有项目、智能体和配置。

### 钻机 (Rigs) 🏗️

项目容器。每个钻机包装一个 git 仓库并管理其关联的智能体。

### 成员 (Crew Members) 👤

您在钻机中的个人工作空间，进行实际操作的地方。

### 臭鼬 (Polecats) 🦨

临时工作智能体，生成后完成任务即消失。

### 钩子 (Hooks) 🪝

基于 git worktree 的智能体工作持久化存储，可在崩溃和重启后存活。

### 车队 (Convoys) 🚚

工作追踪单元，打包多个 bead 分配给智能体。

### Beads 集成 📿

基于 git 的问题追踪系统，将工作状态存储为结构化数据。

## 安装

### 前置要求

- **Go 1.23+**
- **Git 2.25+**
- **beads (bd) 0.44.0+**
- **sqlite3**
- **tmux 3.0+**（推荐）
- **Claude Code CLI**（默认运行时）
- **Codex CLI**（可选运行时）

### 安装步骤

```bash
# 安装 Gas Town
go install github.com/steveyegge/gastown/cmd/gt@latest

# 将 Go 二进制添加到 PATH（添加到 ~/.zshrc 或 ~/.bashrc）
export PATH="$PATH:$HOME/go/bin"

# 创建工作空间并初始化 git
gt install ~/gt --git
cd ~/gt

# 添加第一个项目
gt rig add myproject https://github.com/you/repo.git

# 创建您的成员工作空间
gt crew add yourname --rig myproject
cd myproject/crew/yourname

# 启动市长会话（您的主界面）
gt mayor attach
```

## 快速开始

```shell
gt install ~/gt --git && 
cd ~/gt && 
gt config agent list && 
gt mayor attach
```

然后告诉市长您想构建什么！

## 常用命令

### 工作空间管理

```bash
gt install <path>           # 初始化工作空间
gt rig add <name> <repo>    # 添加项目
gt rig list                 # 列出项目
gt crew add <name> --rig <rig>  # 创建成员工作空间
```

### 智能体操作

```bash
gt agents                   # 列出活跃智能体
gt sling <bead-id> <rig>    # 分配工作给智能体
gt mayor attach             # 启动市长会话
gt prime                    # 上下文恢复
```

### 车队（工作追踪）

```bash
gt convoy create <name> [issues...]   # 创建车队
gt convoy list              # 列出所有车队
gt convoy show [id]         # 显示车队详情
gt convoy add <convoy-id> <issue-id...>  # 添加问题到车队
```

## 架构

```
┌─────────────────────────────────────────────────────────┐
│                      CLI (cobra)                        │
│              agent | gateway | onboard | status          │
└──────┬──────────────────┬───────────────────────────────┘
       │                  │
       ▼                  ▼
┌──────────────┐  ┌───────────────────────────────────────┐
│  Agent Mode  │  │              Gateway                  │
│  (single /   │  │                                       │
│   REPL)      │  │  ┌─────────┐  ┌──────┐  ┌─────────┐  │
└──────┬───────┘  │  │ Channel │  │ Cron │  │Heartbeat│  │
       │          │  │ Manager │  │      │  │         │  │
       │          │  └────┬────┘  └──┬───┘  └────┬────┘  │
       │          │       │          │           │        │
       ▼          │       ▼          ▼           ▼        │
┌──────────────┐  │  ┌─────────────────────────────────┐  │
│  agentsdk-go │  │  │          Message Bus             │  │
│   Runtime    │◄─┤  │    Inbound ←── Channels          │  │
│              │  │  │    Outbound ──► Channels          │  │
└──────────────┘  │  └──────────────────────────────────┘  │
                  └───────────────────────────────────────┘
```

## 使用技巧

- **始终从市长开始**——它是您的主界面
- **使用车队协调**——提供跨智能体可见性
- **利用钩子持久化**——工作不会丢失
- **创建公式重复任务**——使用 Beads 配方节省时间

## 许可证

MIT License - 详见 LICENSE 文件
