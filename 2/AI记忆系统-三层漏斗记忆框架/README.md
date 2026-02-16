# 🧠 AI记忆系统

**仿生AI记忆管理框架** - 让AI像人类一样记住重要信息，忘记无关内容

![系统架构](image/image.png)

---

## 🎯 解决什么问题

传统AI对话系统面临的三大记忆难题：
- **💸 存储困境**：全部记住太贵，快速遗忘又破坏对话连续性
- **🗑️ 信息噪音**：无法区分有价值的内容和闲聊废话
- **❄️ 冷启动**：每次对话从零开始，无法建立长期关系

**AI记忆系统**通过仿生架构自动管理记忆生命周期，就像人类大脑一样工作。

---

## ✨ 核心特性

### 🧠 三层漏斗架构

模拟人类记忆过程，实现三级过滤：

```
┌─────────────────────────────────────────────┐
│  短期记忆(STM)   │  Redis滑动窗口            │
│  ↓ 最近对话      │  默认7天自动过期          │
├─────────────────────────────────────────────┤
│  缓冲区域        │  多维度过滤               │
│  ↓ 价值判断      │  • 重复次数验证           │
│                │  • 时间窗口冷却           │
│                │  • AI智能评分             │
├─────────────────────────────────────────────┤
│  长期记忆(LTM)   │  Qdrant向量数据库         │
│  ✓ 核心知识      │  支持语义搜索             │
└─────────────────────────────────────────────┘
```

### 🎯 智能价值判断

- **多维评分**：AI评估记忆的重要性、相关性和独特性
- **重复验证**：跨会话重复出现的内容更可能重要
- **时间冷却**：防止冲动判断，确保稳定性
- **置信度分级**：高置信度自动晋级，低价值自动丢弃

### ♻️ 语义去重

- 缓冲区去重：防止重复记忆进入漏斗
- 晋升前检查：最终存储前确保唯一性
- 混合方案：向量相似度 + AI语义比较

### 📉 自动遗忘机制

- **艾宾浩斯遗忘曲线**：模拟自然记忆衰减
- **可配置半衰期**：根据使用场景调整衰减速度
- **自动清理**：删除低于阈值分数的低价值记忆

---

## 🚀 快速开始

### 环境要求

- Go 1.25+
- Redis 7.0+
- MySQL 8.0+
- Qdrant 1.0+（向量数据库）
- OpenAI API密钥

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/xwj-vic/AI-Memory.git
cd AI-Memory

# 配置环境变量
cp .env.example .env
# 编辑.env设置API密钥和数据库连接

# 初始化数据库
mysql -u root -p < schema.sql

# 安装依赖并构建
go mod download
go build -o ai-memory

# 启动服务
./ai-memory
```

服务启动后访问 `http://localhost:8080`

默认管理员账号：
- 用户名：`admin`
- 密码：`admin123`

### 🐳 Docker部署（推荐）

```bash
git clone https://github.com/xwj-vic/AI-Memory.git
cd AI-Memory

cp .env.example .env
# 编辑.env设置OPENAI_API_KEY

cd docker && docker-compose up -d
```

这将启动：
- **AI记忆系统** 端口8080
- **Redis** 短期记忆
- **MySQL** 元数据和指标
- **Qdrant** 向量搜索

---

## 💡 使用示例

### 添加记忆

```bash
curl -X POST http://localhost:8080/api/memory/add \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "session_id": "session456",
    "input": "我喜欢在山里徒步",
    "output": "听起来很棒！你通常去哪座山？",
    "metadata": {"topic": "爱好"}
  }'
```

### 检索相关记忆

```bash
curl -X GET "http://localhost:8080/api/memory/retrieve?user_id=user123&query=户外活动&limit=5"
```

### 响应格式

```json
{
  "memories": [
    {
      "id": "uuid-xxxx",
      "content": "用户喜欢在山里徒步",
      "type": "ltm",
      "metadata": {
        "ltm_metadata": {
          "importance": 0.85,
          "last_accessed": "2025-12-16T10:30:00Z",
          "access_count": 12
        }
      },
      "created_at": "2025-12-01T08:00:00Z"
    }
  ]
}
```

---

## ⚙️ 核心配置

`.env`文件关键配置项：

### 记忆漏斗设置

```bash
# 短期记忆(STM)配置
STM_EXPIRATION_DAYS=7              # N天后自动过期
STM_WINDOW_SIZE=100               # 最近消息最大数量
STM_BATCH_JUDGE_SIZE=10           # 批处理大小
STM_JUDGE_MIN_MESSAGES=5          # 触发判断的消息数
STM_JUDGE_MAX_WAIT_MINUTES=60     # 触发判断的等待时间

# 缓冲区域
STAGING_MIN_OCCURRENCES=2         # 需要重复次数
STAGING_MIN_WAIT_HOURS=48         # 冷却期
STAGING_VALUE_THRESHOLD=0.6       # 晋升最低分数
STAGING_CONFIDENCE_HIGH=0.8       # 自动晋升阈值
STAGING_CONFIDENCE_LOW=0.5        # 自动丢弃阈值

# 长期记忆(LTM)衰减
LTM_DECAY_HALF_LIFE_DAYS=90       # 半衰期天数
LTM_DECAY_MIN_SCORE=0.3           # 驱逐阈值
```

### AI模型配置

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=你的密钥
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
```

> 💡 **省钱技巧**：判断任务用`gpt-4o-mini`，关键提取任务再用`gpt-4o`

---

## 📁 项目结构

```
ai-memory/
├── cmd/                    # 命令行工具
├── pkg/
│   ├── api/               # REST API处理器
│   ├── auth/              # 认证服务
│   ├── config/            # 配置加载
│   ├── llm/               # AI模型客户端
│   ├── logger/            # 结构化日志
│   ├── memory/            # 核心记忆逻辑
│   │   ├── manager.go     # 记忆管理器
│   │   ├── funnel.go      # 漏斗系统逻辑
│   │   ├── ltm_dedup.go   # 长期记忆去重
│   │   └── interfaces.go  # 抽象接口
│   ├── store/             # 存储实现
│   │   ├── redis.go       # Redis短期记忆
│   │   ├── qdrant.go      # 向量数据库
│   │   ├── mysql.go       # MySQL元数据
│   │   └── staging_store.go # 缓冲区逻辑
│   └── types/             # 共享数据模型
├── frontend/              # Vue.js管理后台
├── schema.sql             # MySQL数据库结构
├── .env.example           # 配置模板
└── main.go                # 程序入口
```

---

## 📄 许可证

MIT许可证 - 详见[LICENSE](LICENSE)文件

---

<p align="center">用❤️为AI社区打造</p>
