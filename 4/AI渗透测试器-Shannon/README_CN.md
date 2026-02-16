# Shannon - 您的全自主 AI 渗透测试器

<div align="center">

Shannon 的工作很简单：在其他人之前攻破您的 Web 应用。

每个 Claude（编码者）都值得拥有自己的 Shannon。

---

[官网](https://keygraph.io) • [Discord](https://discord.gg/KAqzSHHpRt)

---

</div>

## 🎯 什么是 Shannon？

Shannon 是一个 AI 渗透测试器，提供实际的漏洞利用，而不仅仅是警报。

Shannon 的目标是在其他人之前攻破您的 Web 应用。它自主搜索代码中的攻击向量，然后使用内置浏览器执行真实的漏洞利用，如注入攻击和认证绕过，以证明漏洞确实可被利用。

**Shannon 解决什么问题？**

感谢 Claude Code 和 Cursor 等工具，您的团队不停地发布代码。但您的渗透测试呢？一年才做一次。这造成了*巨大*的安全差距。在其余 364 天里，您可能不知不觉地将漏洞发布到生产环境。

Shannon 通过作为您的按需白盒渗透测试器来弥补这一差距。它不仅发现潜在问题，还执行真实的漏洞利用，提供漏洞的具体证明。这让您可以自信地发布，知道每个构建都是安全的。

## ✨ 功能特性

- **完全自主运行**：单命令启动渗透测试。AI 处理一切，从高级 2FA/TOTP 登录（包括 Google 登录）和浏览器导航到最终报告，零干预。
- **渗透测试级报告与可复现漏洞利用**：交付专注于已验证、可利用发现的最终报告，包含可复制粘贴的概念验证，消除误报，提供可操作的结果。
- **关键 OWASP 漏洞覆盖**：当前识别并验证以下关键漏洞：注入、XSS、SSRF 和认证/授权失效，更多类型开发中。
- **代码感知动态测试**：分析源代码智能引导攻击策略，然后在运行的应用程序上执行实时的浏览器和命令行漏洞利用，确认真实风险。
- **集成安全工具支持**：通过集成领先的侦察和测试工具增强发现阶段——包括 **Nmap、Subfinder、WhatWeb 和 Schemathesis**——深入分析目标环境。
- **并行处理加速结果**：更快获得报告。系统并行化最耗时的阶段，同时运行所有漏洞类型的分析和利用。

## 📦 产品线

Shannon 提供两个版本：

| 版本 | 许可证 | 适用场景 |
|------|--------|----------|
| **Shannon Lite** | AGPL-3.0 | 安全团队、独立研究人员、测试自己的应用 |
| **Shannon Pro** | 商业 | 需要高级功能、CI/CD 集成和专属支持的企业 |

> **本仓库包含 Shannon Lite**，使用我们的核心自主 AI 渗透测试框架。**Shannon Pro** 在此基础上增强了先进的、LLM 驱动的数据流分析引擎，实现企业级代码分析和更深入的漏洞检测。

> **重要提示：仅限白盒。** Shannon Lite 设计用于**白盒（源码可用）**应用程序安全测试。它需要访问您的应用程序源代码和仓库布局。

## 🚀 设置与使用指南

### 前置要求

- **Docker** - 容器运行时
- **AI 提供商凭证**（选择一个）：
  - **Anthropic API 密钥**（推荐）
  - **Claude Code OAuth 令牌**
  - **[实验性 - 不支持] 通过路由器模式的替代提供商**

### 快速开始

```bash
# 1. 克隆 Shannon
git clone https://github.com/KeygraphHQ/shannon.git
cd shannon

# 2. 配置凭证（选择一种方式）

# 方式 A：导出环境变量
export ANTHROPIC_API_KEY="your-api-key"
export CLAUDE_CODE_MAX_OUTPUT_TOKENS=64000

# 方式 B：创建 .env 文件
cat > .env << 'EOF'
ANTHROPIC_API_KEY=your-api-key
CLAUDE_CODE_MAX_OUTPUT_TOKENS=64000
EOF

# 3. 运行渗透测试
./shannon start URL=https://your-app.com REPO=your-repo
```

### 监控进度

```bash
# 查看实时工作日志
./shannon logs

# 查询特定工作流进度
./shannon query ID=shannon-1234567890

# 打开 Temporal Web UI 进行详细监控
open http://localhost:8233
```

### 停止 Shannon

```bash
# 停止所有容器（保留工作流数据）
./shannon stop

# 完全清理（删除所有数据）
./shannon stop CLEAN=true
```

## 📊 示例报告

### 🧃 OWASP Juice Shop

一个众所周知的易受攻击 Web 应用程序，用于测试工具发现各种现代漏洞的能力。

**表现**：在单次自动化运行中，识别出**超过 20 个高影响漏洞**。

**关键成就**：
- 完全绕过认证并通过注入攻击窃取整个用户数据库
- 通过注册流程绕过创建新管理员账户实现完全权限提升
- 发现并利用系统性授权缺陷（IDOR）访问和修改任何用户的私人数据

📄 **[查看完整报告 →](sample-reports/shannon-report-juice-shop.md)**

## 🏗️ 架构

Shannon 使用复杂的多智能体架构模拟人类渗透测试员的方法论。它结合白盒源代码分析和黑盒动态漏洞利用，分为四个不同阶段：

```
                ┌──────────────────────┐
                │    Reconnaissance    │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────┴───────────┐
                │          │           │
                ▼          ▼           ▼
    ┌─────────────────┐ ┌─────────────────┐
    │ Vuln Analysis   │ │ Vuln Analysis   │
    │  (Injection)    │ │     (XSS)       │
    └─────────┬───────┘ └─────────┬───────┘
              │                   │
              ▼                   ▼
    ┌─────────────────┐ ┌─────────────────┐
    │  Exploitation   │ │  Exploitation   │
    │  (Injection)    │ │     (XSS)       │
    └─────────┬───────┘ └─────────┬───────┘
              │                   │
              └─────────┬─────────┘
                        │
                        ▼
                ┌──────────────────────┐
                │      Reporting       │
                └──────────────────────┘
```

### 阶段说明

**阶段 1：侦察** - 构建应用程序攻击面的完整地图
**阶段 2：漏洞分析** - 并行分析潜在缺陷
**阶段 3：漏洞利用** - 将假设转化为概念验证
**阶段 4：报告** - 编制专业、可操作的报告

## ⚠️ 免责声明

### 重要使用指南和免责声明

请在使用 Shannon (Lite) 前仔细阅读以下指南。作为用户，您需对自己的行为负责并承担所有责任。

#### 1. 潜在的变异效应与环境选择

这不是被动扫描器。漏洞利用智能体设计用于**主动执行攻击**以确认漏洞。此过程可能对目标应用程序及其数据产生变异效应。

> ⚠️ **请勿在生产环境运行 Shannon。**
>
> - 它仅适用于沙箱、测试或本地开发环境，这些环境中数据完整性不是问题。
> - 潜在变异效应包括但不限于：创建新用户、修改或删除数据、破坏测试账户、注入攻击触发意外副作用。

#### 2. 法律与道德使用

Shannon 仅供合法的安全审计目的使用。

> 您必须获得目标系统所有者的**明确书面授权**后才能运行 Shannon。
>
> 未经授权扫描和利用您不拥有的系统是非法的。Keygraph 对 Shannon 的任何滥用不承担责任。

#### 3. LLM 与自动化注意事项

- **需要验证**：虽然我们通过"利用证明"方法论消除误报，但底层 LLM 仍可能在最终报告中产生幻觉或弱支持内容。**人工监督至关重要**。
- **全面性**：Shannon Lite 的分析可能因 LLM 上下文窗口固有限制而不全面。

#### 4. 成本与性能

- **时间**：完整测试运行通常需要 **1 到 1.5 小时**
- **成本**：使用 Anthropic Claude 4.5 Sonnet 模型运行完整测试可能产生约 **$50 美元**费用

## 📜 许可证

Shannon Lite 采用 [GNU Affero General Public License v3.0 (AGPL-3.0)](LICENSE) 发布。

Shannon 是开源的（AGPL v3）。此许可证允许您：
- 自由用于所有内部安全测试
- 私下修改代码供内部使用而无需共享更改

AGPL 的共享要求主要适用于将 Shannon 作为公共或托管服务（如 SaaS 平台）提供的组织。在那些特定情况下，对核心软件的任何修改必须开源。

## 👥 社区与支持

- 🐛 **报告错误**：[GitHub Issues](https://github.com/KeygraphHQ/shannon/issues)
- 💡 **建议功能**：[Discussions](https://github.com/KeygraphHQ/shannon/discussions)
- 💬 **Discord**：[加入社区](https://discord.gg/KAqzSHHpRt)
- 🐦 **Twitter**：[@KeygraphHQ](https://twitter.com/KeygraphHQ)
- 🌐 **官网**：[keygraph.io](https://keygraph.io)
