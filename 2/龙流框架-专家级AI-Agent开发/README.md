# 龙流框架：专家级AI智能体开发平台

<div align="center">

**释放创造力！龙流框架将你的专业知识转化为AI生产力。**

龙流是一个开源的**专家级智能体开发框架**。

通过PES范式（规划-执行-总结）让智能体具备思考和学习能力，并通过迭代积累经验。

</div>

---

## ✨ 为什么选龙流？

**一个会思考、会学习的专家级智能体框架。它赋予智能体像科学家一样的思考能力，帮助开发者快速将专业知识转化为专家级智能体。**

- **智能思考**：创新的PES（规划-执行-总结）范式。龙流赋予智能体结构化思维，应对长程复杂推理挑战。这让智能体能够以人类科学家的严谨思维迭代处理高难度任务。
- **持续学习**：创新的多结构融合记忆。通过主动生成模型推理上下文，龙流让智能体在任务迭代中持续综合经验。形成"边跑边改进"的机制，实现轻量级学习和进化，无需繁重重训练。

> 我们相信，设计一个能够解决复杂问题的专家级智能体的关键在于**智能体的思维范式**。思维范式决定了智能体能处理的问题复杂度，并设定了其效能上限。龙流专为需要长程推理的复杂任务而构建，帮助开发者快速构建具备领域专家性能的AI。

---

## 🚀 快速开始

### 安装

> 龙流需要 **Python 3.12** 或更高版本。

```bash
# 安装uv/conda并克隆仓库
# uv: https://docs.astral.sh/uv/getting-started/installation/
# Miniforge: https://conda-forge.org/download/

# 使用uv安装
cd LoongFlow
uv venv .venv --python 3.12
source .venv/bin/activate
uv pip install -e .

# 使用conda安装
cd LoongFlow
conda create -n loongflow python=3.12
conda activate loongflow
pip install -e .
```

### 运行示例

#### 数学智能体

```bash
# 配置LLM：编辑task_config.yaml，推荐使用gemini-3-pro-preview或deepseek-r1-250528
# 示例：./agents/math_agent/examples/packing_circle_in_unit_square/task_config.yaml
# 模型需要按需配置服务商，默认服务商是openai。例如：openai/gemini-3-pro-preview
llm_config:
  url: "https://xxxxxx/v1"
  api_key: "******"
  model: "openai/gemini-3-pro-preview"

# 运行第一个进化任务，进化结果在./output目录
uv pip install -r ./agents/math_agent/examples/packing_circle_in_unit_square/requirements.txt
./run_math.sh packing_circle_in_unit_square --background

# 查看任务日志
tail -f ./agents/math_agent/examples/packing_circle_in_unit_square/run.log

# 停止任务
./run_math.sh stop packing_circle_in_unit_square
```

#### 机器学习智能体

```bash
# 配置LLM：编辑task_config.yaml，推荐使用gemini-3-pro-preview或deepseek-r1-250528
# 示例：./agents/ml_agent/examples/ml_example/task_config.yaml
# 模型需要按需配置服务商，默认服务商是openai。例如：openai/gemini-3-pro-preview
llm_config:
  url: "https://xxxxxx/v1"
  api_key: "******"
  model: "openai/gemini-3-pro-preview"

# 初始化ML进化
./run_ml.sh init

# 运行第一个进化任务，进化结果在./output目录
# ./run_ml.sh run <task_name> [--background] [其他Python参数]
./run_ml.sh run ml_example --background

# 查看任务日志
tail -f ./agents/ml_agent/examples/ml_example/agent.log

# 停止任务
./run_ml.sh stop ml_example
```

---

## 🧠 龙流如何工作

龙流围绕一个简单的理念设计：

> 专家级性能不是来自更好的变异，而是来自更好的思考、反思和经验积累。

为此，龙流将智能体行为组织成思考-学习-进化循环。

### PES思维范式

龙流的核心是**PES（规划-执行-总结）思维范式**，灵感来自人类专家的研究方式：

| 阶段 | 内容 |
|------|------|
| **规划** | • 理解任务和约束<br>• 检索相关过往经验<br>• 设计清晰高质量的执行蓝图<br><br>> 规划确保生成是深思熟虑的而非盲目 |
| **执行** | • 进行结构化实验<br>• 验证中间结果<br>• 避免低价值或冗余尝试<br><br>> 执行成为受控实验，而非猜测 |
| **总结** | • 深度反思成功与失败<br>• 提取可复用的洞见<br>• 将经验持久化为结构化记忆<br><br>> 总结防止智能体重复同样的错误 |

PES将进化从变异驱动过程转变为**推理引导的改进循环**。

### 学习与进化记忆

仅有思考是不够的。为了持续提升，智能体必须**记住、泛化并逃离局部最优**。

龙流将PES与混合进化记忆系统集成：
- 多岛 + MAP-Elites保持多样性
- 自适应玻尔兹曼选择平衡探索与利用
- 全局进化树记忆用于长程经验检索

这让智能体能够进行**跳跃式推理**——利用过去的发现超越增量局部搜索。

---

## 🏆 已验证成就

### 数学挑战（Tao & AlphaEvolve数据集）

在几何和代数的11项挑战中，龙流超越了所有已知最佳结果，并在7个特定问题上超越AlphaEvolve，达到最新SOTA。

### MLE-bench（Kaggle竞赛）

在MLE-bench的全部48场Kaggle竞赛中获得奖牌，包括26枚金牌。

---

## 🧩 高级用法

### PES智能体

```python
from loongflow.framework.pes import PESAgent

# 配置进化智能体
agent = PESAgent(
    config=config,
    checkpoint_path=checkpoint_path,
)

# 注册工作器（实现Planner、Executor、Summary接口）
agent.register_planner_worker("planner", PlanAgent)
agent.register_executor_worker("executor", ExecuteAgent)
agent.register_summary_worker("summary", SummaryAgent)

# 运行智能体
result = await agent()
```

### ReAct智能体

```python
from loongflow.framework.react import AgentContext, ReActAgent
from loongflow.agentsdk.tools import TodoReadTool, TodoWriteTool, Toolkit

# 构建智能体上下文
toolkit = Toolkit()
toolkit.register_tool(TodoReadTool())
toolkit.register_tool(TodoWriteTool())

# 构建默认react智能体
agent = ReActAgent.create_default(model=model, sys_prompt=sys_prompt, toolkit=toolkit)

# 运行智能体
result = await agent(message)
```

---

## 📊 可视化

**实时进化追踪**，交互式Web界面：

```bash
# 启动可视化服务器
python agents/math_agent/visualizer/visualizer.py --port 8888 --checkpoint-path output-circle-packing/database/checkpoints
```

**功能：**
- 🌳 展示父子关系的进化树
- 📈 多代性能追踪
- 🔍 显示变异的代码差异查看器
- 📊 解决方案分布的岛屿图

---

## 💰 运行成本

以CirclePacking问题为例，如果使用Gemini 3 Pro，总成本约**$10**。

---

## 📜 许可证

Apache License 2.0

---

<div align="center">

### **🚀 准备好构建你的专家智能体了吗？**

**由龙流社区维护**

_如果龙流对你有帮助，请考虑为仓库点星。_

</div>
