# myclaw

**基于 [agentsdk-go](https://github.com/cexll/agentsdk-go) 构建的个人 AI 助手。**

## 功能特性

- **CLI 智能体** - 单消息或交互式 REPL 模式
- **网关** - 完整编排：频道 + 定时任务 + 心跳
- **Telegram 频道** - 通过 Telegram 机器人接收和发送消息（文本 + 图片 + 文档）
- **飞书频道** - 通过飞书（Lark）机器人接收和发送消息
- **企业微信频道** - 通过企业微信智能机器人 API 模式接收消息并发送 Markdown 回复
- **WhatsApp 频道** - 通过 WhatsApp 接收和发送消息（二维码登录）
- **Web UI** - 基于 WebSocket 的浏览器聊天界面（响应式，支持 PC + 移动端）
- **多提供商** - 支持 Anthropic 和 OpenAI 模型
- **多模态** - 图像识别和文档处理
- **定时任务** - JSON 持久化的计划任务
- **心跳** - 来自 HEARTBEAT.md 的周期性任务
- **记忆** - 长期（MEMORY.md）+ 每日记忆
- **技能** - 从工作区加载自定义技能

## 快速开始

```bash
# 构建
make build

# 构建更小的发布版本
make build-release

# 交互式配置设置
make setup

# 或手动初始化配置和工作区
make onboard

# 设置 API 密钥
export MYCLAW_API_KEY=your-api-key

# 运行智能体（单消息）
./myclaw agent -m "你好"

# 运行智能体（REPL 模式）
make run

# 启动网关（频道 + 定时任务 + 心跳）
make gateway
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

## 项目结构

```
cmd/myclaw/          CLI 入口点（agent, gateway, onboard, status）
internal/
  bus/               消息总线（入站/出站频道）
  channel/           频道接口 + 实现
    telegram.go      Telegram 机器人
    feishu.go        飞书/Lark 机器人
    wecom.go         企业微信智能机器人
    whatsapp.go      WhatsApp
    webui.go         Web UI（WebSocket）
  config/            配置加载（JSON + 环境变量）
  cron/              定时任务调度
  gateway/           网关编排
  heartbeat/         周期性心跳服务
  memory/            记忆系统
  skills/            自定义技能加载器
```

## 配置

运行 `make setup` 进行交互式配置，或将 `config.example.json` 复制到 `~/.myclaw/config.json`：

```json
{
  "provider": {
    "type": "anthropic",
    "apiKey": "your-api-key",
    "baseUrl": ""
  },
  "agent": {
    "model": "claude-sonnet-4-5-20250929"
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "your-bot-token",
      "allowFrom": ["123456789"]
    },
    "feishu": {
      "enabled": true,
      "appId": "cli_xxx",
      "appSecret": "your-app-secret"
    },
    "wecom": {
      "enabled": true,
      "token": "your-token",
      "encodingAESKey": "your-43-char-encoding-aes-key"
    },
    "whatsapp": {
      "enabled": true
    },
    "webui": {
      "enabled": true
    }
  }
}
```

## 频道设置

### Telegram

1. 通过 Telegram 上的 [@BotFather](https://t.me/BotFather) 创建机器人
2. 在配置中设置 `token` 或 `MYCLAW_TELEGRAM_TOKEN` 环境变量
3. 运行 `make gateway`

### 飞书 (Lark)

1. 在 [飞书开放平台](https://open.feishu.cn/app) 创建应用
2. 启用**机器人**能力
3. 添加权限：`im:message`, `im:message:send_as_bot`
4. 配置事件订阅 URL：`https://your-domain/feishu/webhook`
5. 设置 `appId`, `appSecret`, `verificationToken`

### 企业微信

1. 在 API 模式下创建企业微信智能机器人，获取 `token`, `encodingAESKey`
2. 配置回调 URL：`https://your-domain/wecom/bot`
3. 设置 `token` 和 `encodingAESKey`

### WhatsApp

1. 设置 `"whatsapp": {"enabled": true}`
2. 运行 `make gateway`
3. 用 WhatsApp 扫描终端显示的二维码

### Web UI

1. 设置 `"webui": {"enabled": true}`
2. 运行 `make gateway`
3. 在浏览器打开 `http://localhost:18790`

## Docker 部署

```bash
docker build -t myclaw .

docker run -d \
  -e MYCLAW_API_KEY=your-api-key \
  -e MYCLAW_TELEGRAM_TOKEN=your-token \
  -p 18790:18790 \
  -p 9876:9876 \
  -p 9886:9886 \
  -v myclaw-data:/root/.myclaw \
  myclaw
```

## 测试

```bash
make test            # 运行所有测试
make test-race       # 带竞态检测运行
make test-cover      # 带覆盖率报告运行
make lint            # 运行 golangci-lint
```

## 许可证

MIT
