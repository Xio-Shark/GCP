# GitHub 智能体工作流

**使用自然语言 Markdown 编写智能体工作流，并在 GitHub Actions 中运行。**

## 目录

- [快速开始](#快速开始)
- [概述](#概述)
- [防护机制](#防护机制)
- [文档](#文档)
- [贡献](#贡献)
- [反馈](#反馈)
- [Peli 的智能体工厂](#pelis-智能体工厂)

## 快速开始

准备好运行您的第一个智能体工作流了吗？请按照我们的分步[快速开始指南](https://github.github.com/gh-aw/setup/quick-start/)安装扩展、添加示例工作流并查看实际运行效果。

## 概述

了解智能体工作流背后的概念，探索可用的工作流类型，了解 AI 如何自动化您的仓库任务。请参阅[工作原理](https://github.github.com/gh-aw/introduction/how-they-work/)。

## 防护机制

防护机制、安全性和安全性是 GitHub 智能体工作流的基础。工作流默认以只读权限运行，写入操作仅允许通过净化的 `safe-outputs` 进行。系统实现多层保护，包括：

- 沙箱执行
- 输入净化
- 网络隔离
- 供应链安全（SHA 固定依赖）
- 工具白名单
- 编译时验证
- 可限制为仅团队成员访问
- 关键操作的人工审批门控

确保 AI 智能体在受控边界内安全运行。请参阅[安全架构](https://github.github.com/gh-aw/introduction/architecture/)了解威胁建模、实施指南和最佳实践的完整详情。

**重要提示**：在仓库中使用智能体工作流需要仔细注意安全考虑事项和人工监督，即使如此仍可能出现问题。请谨慎使用，风险自负。

## 文档

完整文档、示例和指南，请参阅[文档站点](https://github.github.com/gh-aw/)。

## 贡献

开发设置和贡献指南，请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 反馈

我们欢迎您对 GitHub 智能体工作流的反馈！

- [社区反馈讨论](https://github.com/orgs/community/discussions/186451)
- [GitHub Next Discord](https://gh.io/next-discord)

## Peli 的智能体工厂

请参阅 [Peli 的智能体工厂](https://github.github.com/gh-aw/blog/2026-01-12-welcome-to-pelis-agent-factory/)，了解智能体工作流多种用法的导览。

## 相关项目

GitHub 智能体工作流由配套项目支持，提供额外的安全和集成能力：

- **[智能体工作流防火墙 (AWF)](https://github.com/github/gh-aw-firewall)** - AI 智能体的网络出口控制，提供基于域名的访问控制和活动日志记录
- **[MCP 网关](https://github.com/github/gh-aw-mcpg)** - 通过统一的 HTTP 网关路由模型上下文协议 (MCP) 服务器调用，实现集中访问管理

## 核心特性

- **自然语言编写**：使用 Markdown 编写工作流，无需复杂编程
- **GitHub Actions 集成**：直接在 GitHub 生态系统中运行
- **安全优先**：多层安全防护机制
- **AI 驱动**：利用 AI 自动化处理仓库任务
- **可扩展**：支持多种工作流类型和自定义配置

## 适用场景

- 自动化代码审查
- 自动化问题分类和处理
- 文档自动生成和更新
- 代码重构和优化建议
- 安全漏洞扫描和修复建议
- 自动化测试生成
