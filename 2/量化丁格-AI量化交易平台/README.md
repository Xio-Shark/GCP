# 量化丁格

<div align="center">

<img src="https://ai.quantdinger.com/img/logo.e0f510a8.png" alt="量化丁格Logo" width="160" height="160">

**下一代AI量化交易平台**

🤖 AI原生 · 🐍 可视化Python · 🌍 多市场 · 🔒 隐私优先

用AI副驾驶构建、回测和交易。比PineScript更好用，比SaaS更智能。

</div>

---

## 📖 介绍

### 什么是量化丁格？

量化丁格是一个**本地优先、隐私优先、自托管的量化交易基础设施**。它运行在你自己的机器/服务器上，提供**基于PostgreSQL的多用户账户**，同时让你完全掌控策略、交易数据和API密钥。

### 为什么是本地优先？

与将数据和策略锁定在云端的SaaS平台不同，量化丁格在本地运行。你的策略、交易日志、API密钥和分析结果都保留在你的机器上。无供应商锁定，无订阅费用，无数据外泄。

### 适合谁？

量化丁格为重视以下因素的**交易者、研究人员和工程师**而构建：
- 数据主权和隐私
- 透明、可审计的交易基础设施
- 工程优先于营销
- 完整的工作流：数据、分析、回测和执行

### 核心价值

- **🔓 Apache 2.0开源（代码）**：宽松且商业友好。你可以在Apache 2.0下fork和修改代码库，同时保留必要的声明。
- **🐍 Python原生 & 可视化**：用标准Python（比PineScript更容易）编写指标，借助AI辅助。直接在K线图上可视化信号——"本地版TradingView"体验。
- **🤖 AI循环优化**：它不仅运行策略；AI分析回测结果以建议参数调整（止损/止盈/MACD设置），形成闭环优化。
- **🌍 通用市场接入**：加密货币（实盘）、美股/港股、外汇、期货（数据/通知）统一系统。
- **⚡ Docker & 整洁架构**：4行命令部署。现代技术栈（Vue + Python）架构清晰、关注点分离。

---

## 🚀 快速开始

### 方式一：Docker部署（推荐）

使用PostgreSQL数据库和多用户支持运行量化丁格的最快方式。

#### 1. 配置环境

在项目根目录创建`.env`文件：

```bash
# 数据库配置
POSTGRES_USER=quantdinger
POSTGRES_PASSWORD=你的安全密码
POSTGRES_DB=quantdinger

# 管理员账户（首次启动时创建）
ADMIN_USER=quantdinger
ADMIN_PASSWORD=123456

# 可选：AI功能
OPENROUTER_API_KEY=你的API密钥
```

#### 2. 启动服务

**Linux / macOS**
```bash
git clone https://github.com/brokermr810/QuantDinger.git && \
cd QuantDinger && \
cp backend_api_python/env.example backend_api_python/.env && \
docker-compose up -d --build
```

**Windows (PowerShell)**
```powershell
git clone https://github.com/brokermr810/QuantDinger.git
cd QuantDinger
Copy-Item backend_api_python\env.example -Destination backend_api_python\.env
docker-compose up -d --build
```

这将自动：
- 启动PostgreSQL数据库（端口5432）
- 初始化数据库结构
- 启动后端API（端口5000）
- 启动前端（端口8888）
- 从`.env`的`ADMIN_USER`/`ADMIN_PASSWORD`创建管理员用户

#### 3. 访问应用

- **前端界面**: http://localhost:8888
- **后端API**: http://localhost:5000
- **默认账户**: 使用`.env`中的`ADMIN_USER` / `ADMIN_PASSWORD`（默认：`quantdinger` / `123456`，生产环境请修改）

> **注意**：生产环境请编辑`backend_api_python/.env`设置强密码，添加`OPENROUTER_API_KEY`启用AI功能，然后`docker-compose restart backend`重启。

---

## ✨ 核心功能

### 1. 可视化Python策略工作台
*比PineScript更好用，比SaaS更智能。*

- **Python原生**：用Python编写指标和策略。利用整个Python生态系统（Pandas, Numpy, TA-Lib），而非PineScript等专有语言。
- **"Mini-TradingView"体验**：在内置K线图上直接运行Python指标。在历史数据上可视化调试验买/卖信号。
- **AI辅助编程**：让内置AI为你编写复杂逻辑。从想法到代码只需几秒。

### 2. 完整交易生命周期
*从指标到执行，无缝衔接。*

1. **指标**：定义你的入场/出场信号
2. **策略配置**：附加风险管理规则（仓位大小、止损、止盈）
3. **回测 & AI优化**：运行回测，查看丰富的绩效指标，**让AI分析结果并建议改进**（如"将MACD阈值调整为X"）
4. **执行模式**：
   - **实盘交易**：
     - **加密货币**：10+交易所直接API执行（币安、OKX、Bitget、Bybit等）
     - **美股/港股**：通过盈透证券(IBKR)
     - **外汇**：通过MT5
   - **信号通知**：对于不支持实盘的市场（A股/期货），通过Telegram、Discord、邮件、短信或Webhook发送信号

### 3. AI驱动分析
*快速、准确、专业报告。*

量化丁格提供精简的AI分析系统：

- **快速分析模式**：单LLM调用架构，快速准确分析（替代复杂多智能体系统）
- **全球市场整合**：分析页面集成实时市场数据、热力图和经济日历
- **ATR交易级别**：基于技术分析的止损和止盈建议（ATR、支撑/阻力）
- **分析记忆**：存储分析结果供历史回顾和持续学习
- **策略整合**：AI分析可作为策略的"市场过滤器"

### 4. 通用数据引擎

量化丁格为多市场提供统一的数据接口：

- **加密货币**：交易直接API连接（10+交易所）和CCXT市场数据整合（100+数据源）
- **股票**：美股Yahoo Finance、Finnhub、Tiingo，港股AkShare、东方财富
- **期货/外汇**：OANDA和主要期货数据源
- **代理支持**：内置代理配置，适用于受限网络环境

### 5. 记忆增强智能体（本地RAG + 反思循环）

量化丁格的智能体不会每次都从零开始。后端包括**本地记忆存储**和可选的**反思/验证循环**：

- **是什么**：RAG风格的经验检索注入智能体提示（非模型微调）
- **位置**：PostgreSQL数据库（与主数据共享）或`backend_api_python/data/memory/`下的本地文件（隐私优先）

### 6. 策略运行时

- **基于线程的执行器**：独立的策略执行线程池
- **自动恢复**：系统重启后恢复运行中的策略
- **订单队列**：订单执行的后台工作器

### 7. 多LLM服务商支持

量化丁格支持多种AI服务商自动检测：

| 服务商 | 特点 |
|--------|------|
| **OpenRouter** | 多模型网关（默认），100+模型 |
| **OpenAI** | GPT-4o, GPT-4o-mini |
| **Google Gemini** | Gemini 1.5 Flash/Pro |
| **DeepSeek** | DeepSeek Chat（高性价比） |
| **xAI Grok** | Grok Beta |

只需在`.env`中配置你偏好的服务商API密钥。系统自动检测可用服务商。

### 8. 指标社区
*分享、发现和交易指标。*

- **发布 & 分享**：与社区分享你的Python指标
- **购买系统**：从其他用户购买高级指标
- **评分 & 评论**：对已购指标评分和评论
- **管理审核**：质量控制审核系统

### 9. 用户管理 & 安全

- **多用户支持**：基于PostgreSQL的用户账户和基于角色的权限
- **OAuth登录**：Google和GitHub OAuth整合
- **邮箱验证**：通过邮箱验证码注册和密码重置
- **安全功能**：Cloudflare Turnstile验证码、IP/账户速率限制
- **演示模式**：公共演示的只读模式

---

## 🔌 支持的交易所 & 经纪商

### 加密货币交易所（直接API）

| 交易所 | 市场 |
|:------:|:------|
| 币安 | 现货、期货、杠杆 |
| OKX | 现货、永续、期权 |
| Bitget | 现货、期货、跟单交易 |
| Bybit | 现货、线性期货 |
| Coinbase Exchange | 现货 |
| Kraken | 现货、期货 |
| KuCoin | 现货、期货 |
| Gate.io | 现货、期货 |
| Bitfinex | 现货、衍生品 |

### 传统经纪商

| 经纪商 | 市场 | 平台 |
|:------:|:------|:------|
| **盈透证券(IBKR)** | 美股、港股 | TWS / IB Gateway |
| **MetaTrader 5(MT5)** | 外汇 | MT5终端 |

### 市场数据（通过CCXT）

Bybit、Gate.io、Kraken、KuCoin、火币等100+交易所的市场数据。

---

## 📜 许可证

Apache License 2.0

---

<div align="center">

**享受零记忆损失的编码体验**

</div>
