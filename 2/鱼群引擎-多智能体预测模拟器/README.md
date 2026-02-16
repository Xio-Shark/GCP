# 🐟 鱼群引擎

<div align="center">

<img src="./static/image/MiroFish_logo_compressed.jpeg" alt="鱼群引擎Logo" width="75%"/>

**简洁通用的群体智能引擎，预测万物**

</div>

---

## ⚡ 项目概述

**鱼群引擎**是一款基于多智能体技术的新一代AI预测引擎。通过提取现实世界的种子信息（如突发新闻、政策草案、金融信号），自动构建出高保真的平行数字世界。在此空间内，成千上万个具备独立人格、长期记忆与行为逻辑的智能体进行自由交互与社会演化。你可透过「上帝视角」动态注入变量，精准推演未来走向——**让未来在数字沙盘中预演，助决策在百战模拟后胜出**。

> 你只需：上传种子材料（数据分析报告或者有趣的小说故事），并用自然语言描述预测需求
> 鱼群引擎将返回：一份详尽的预测报告，以及一个可深度交互的高保真数字世界

### 我们的愿景

鱼群引擎致力于打造映射现实的群体智能镜像，通过捕捉个体互动引发的群体涌现，突破传统预测的局限：

- **于宏观**：我们是决策者的预演实验室，让政策与公关在零风险中试错
- **于微观**：我们是个人用户的创意沙盘，无论是推演小说结局还是探索脑洞，皆可有趣、好玩、触手可及

从严肃预测到趣味仿真，我们让每一个如果都能看见结果，让预测万物成为可能。

---

## 🎬 演示视频

### 1. 武汉大学舆情推演预测 + 鱼群引擎项目讲解

点击观看使用微舆BettaFish生成的《武大舆情报告》进行预测的完整演示视频

### 2. 《红楼梦》失传结局推演预测

点击查看基于《红楼梦》前80回数十万字，鱼群引擎深度预测失传结局

> **金融方向推演预测**、**时政要闻推演预测**等示例陆续更新中...

---

## 🔄 工作流程

1. **图谱构建**：现实种子提取 & 个体与群体记忆注入 & GraphRAG构建
2. **环境搭建**：实体关系抽取 & 人设生成 & 环境配置Agent注入仿真参数
3. **开始模拟**：双平台并行模拟 & 自动解析预测需求 & 动态更新时序记忆
4. **报告生成**：ReportAgent拥有丰富的工具集与模拟后环境进行深度交互
5. **深度互动**：与模拟世界中的任意一位进行对话 & 与ReportAgent进行对话

---

## 🚀 快速开始

### 一、源码部署（推荐）

#### 前置要求

| 工具 | 版本要求 | 说明 | 安装检查 |
|------|---------|------|---------|
| **Node.js** | 18+ | 前端运行环境，包含npm | `node -v` |
| **Python** | ≥3.11, ≤3.12 | 后端运行环境 | `python --version` |
| **uv** | 最新版 | Python包管理器 | `uv --version` |

#### 1. 配置环境变量

```bash
# 复制示例配置文件
cp .env.example .env

# 编辑.env文件，填入必要的API密钥
```

**必需的环境变量：**

```env
# LLM API配置（支持OpenAI SDK格式的任意LLM API）
# 推荐使用阿里百炼平台qwen-plus模型：https://bailian.console.aliyun.com/
# 注意消耗较大，可先进行小于40轮的模拟尝试
LLM_API_KEY=你的API密钥
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL_NAME=qwen-plus

# Zep Cloud配置
# 每月免费额度即可支撑简单使用：https://app.getzep.com/
ZEP_API_KEY=你的ZEP密钥
```

#### 2. 安装依赖

```bash
# 一键安装所有依赖（根目录 + 前端 + 后端）
npm run setup:all
```

或者分步安装：

```bash
# 安装Node依赖（根目录 + 前端）
npm run setup

# 安装Python依赖（后端，自动创建虚拟环境）
npm run setup:backend
```

#### 3. 启动服务

```bash
# 同时启动前后端（在项目根目录执行）
npm run dev
```

**服务地址：**
- 前端：`http://localhost:3000`
- 后端API：`http://localhost:5001`

**单独启动：**

```bash
npm run backend   # 仅启动后端
npm run frontend  # 仅启动前端
```

### 二、Docker部署

```bash
# 1. 配置环境变量（同源码部署）
cp .env.example .env

# 2. 拉取镜像并启动
docker compose up -d
```

默认会读取根目录下的`.env`，并映射端口`3000（前端）/5001（后端）`

> 在`docker-compose.yml`中已通过注释提供加速镜像地址，可按需替换

---

## 📄 致谢

**鱼群引擎得到了盛大集团的战略支持和孵化！**

鱼群引擎的仿真引擎由 **[OASIS](https://github.com/camel-ai/oasis)** 驱动，我们衷心感谢CAMEL-AI团队的开源贡献！

---

## 📈 项目统计

<p align="center">
  <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=666ghj/MiroFish&type=date&legend=top-left" />
</p>
