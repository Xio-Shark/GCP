# 神经网络可视化设计器

基于Flask + LiteGraph.js的可视化深度学习训练工作台，支持拖拽构建神经网络架构并生成PyTorch训练代码。

---

## 🌟 主要功能

### 可视化模型设计
- **拖拽式界面**：基于LiteGraph.js的直观节点编辑器
- **可视化连接**：节点间连线一目了然
- **形状推断**：自动计算和显示张量维度变化
- **子图支持**：创建可复用的模块化组件

### 丰富的神经网络层支持
- **基础层**：Conv2D, Linear, MaxPool2D, AvgPool2D, Flatten, Dropout
- **激活函数**：ReLU, GELU, Sigmoid, Tanh, Softmax
- **归一化层**：BatchNorm2D, LayerNorm
- **嵌入层**：Embedding
- **Transformer组件**：多头注意力, GPT块, Transformer编码器
- **损失函数**：CrossEntropyLoss, MSELoss
- **优化器**：Adam, SGD

### 代码生成与训练
- **PyTorch代码生成**：生成完整的训练脚本
- **实时训练监控**：通过WebSocket实时显示训练状态
- **训练可视化**：损失曲线、混淆矩阵、预测结果图表
- **推理应用导出**：生成独立的推理应用

### 数据处理
- **内置数据集**：MNIST手写数字等数据集支持
- **数据加载器**：自动处理数据预处理和批次管理
- **自定义数据**：支持上传自定义数据集

---

## 🚀 快速开始

### 环境要求
- Python 3.8+
- PyTorch
- Flask

### 安装步骤

```bash
# 克隆项目
git clone https://github.com/streetartist/CortexNodus.git
cd CortexNodus

# 安装依赖
pip install -r requirements.txt

# 启动应用
python app.py
```

浏览器访问 `http://localhost:5000`

---

## 📖 使用指南

### 基本工作流程

1. **设计模型架构**
   - 从右侧面板选择神经网络层
   - 拖拽节点到画布
   - 连接节点构建数据流

2. **配置参数**
   - 点击节点设置层参数

3. **生成代码（可选）**
   - 点击"生成代码"按钮
   - 系统生成完整的PyTorch训练脚本

4. **训练模型**
   - 点击"开始训练"
   - 实时监控训练进度和指标

5. **查看结果**
   - 训练完成后自动显示可视化结果
   - 包括损失曲线、混淆矩阵等

### 支持的节点类型

#### 数据层
- **Input**：输入数据节点
- **Target**：目标标签节点

#### 神经网络层
- **Conv2D**：二维卷积层
- **Linear**：全连接层
- **MaxPool2D**：二维最大池化
- **AvgPool2D**：二维平均池化
- **Flatten**：数据展平层
- **Dropout**：随机失活层
- **BatchNorm2D**：二维批归一化
- **LayerNorm**：层归一化
- **Embedding**：嵌入层

#### 激活函数
- **ReLU**：ReLU激活函数
- **GELU**：GELU激活函数
- **Sigmoid**：Sigmoid激活函数
- **Tanh**：Tanh激活函数
- **Softmax**：Softmax激活函数

#### Transformer组件
- **MultiHeadAttention**：多头注意力机制
- **GPTBlock**：GPT风格的Transformer块
- **TransformerEncoder**：Transformer编码器

#### 输出层
- **CrossEntropyLoss**：交叉熵损失函数
- **MSELoss**：均方误差损失函数

---

## 🔧 高级功能

### 子图系统
- 创建可复用的模块化组件
- 将复杂网络封装为单个节点
- 支持子图的导入和导出

### 实时训练监控
- WebSocket实时连接
- 动态更新训练状态
- 实时显示损失值和准确率

### 代码导出
- 生成独立的Python训练脚本
- 支持推理应用导出
- 包含完整的模型定义和训练逻辑

---

## 📁 项目结构

```
神经网络可视化设计器/
├── app.py                 # Flask主应用
├── ml/                    # 机器学习核心模块
│   ├── designer.py        # 节点注册和模型构建
│   ├── code_generator.py  # PyTorch代码生成
│   ├── data_loader.py     # 数据加载和处理
│   └── visualization.py   # 训练可视化
├── static/                # 静态资源
│   ├── designer.js        # 前端节点编辑器
│   ├── style.css          # 样式文件
│   └── plots/             # 生成的图表
├── templates/             # HTML模板
├── example/               # 示例配置
├── subgraphs/             # 子图定义
├── docs/                  # 文档
└── test/                  # 测试文件
```

---

## 🎯 示例项目

### CNN MNIST分类器
1. 创建Input节点 (1, 28, 28)
2. 添加Conv2D → ReLU → MaxPool2D
3. 重复卷积块
4. 添加Flatten → Linear → CrossEntropyLoss
5. 连接Target节点
6. 生成代码并开始训练

### Transformer模型
1. 使用Embedding层处理输入
2. 添加MultiHeadAttention层
3. 使用GPTBlock构建Transformer块
4. 添加输出层和损失函数

---

## 📄 许可证

GPL-3.0许可证 - 详见[LICENSE](LICENSE)文件

---

## 🔗 相关链接

- [LiteGraph.js](https://github.com/jagenjo/litegraph.js) - 可视化节点编辑器
- [PyTorch](https://pytorch.org/) - 深度学习框架
- [Flask](https://flask.palletsprojects.com/) - Web框架
