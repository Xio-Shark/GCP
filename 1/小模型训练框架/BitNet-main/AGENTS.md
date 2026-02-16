# AGENTS.md

此文件包含在该代码库中工作的代理编码指南。

## 构建命令

### 环境设置和构建
```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境并构建（自动处理 CMake 构建和模型准备）
python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s

# 手动 CMake 构建（如果需要）
cmake -B build -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++
cmake --build build --config Release
```

### 运行推理
```bash
# 基本推理
python run_inference.py -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf -p "提示文本" -cnv

# 推理服务器
python run_inference_server.py
```

### 测试命令
```bash
# 运行困惑度测试（在所有数据集上）
python utils/test_perplexity.py -m <model_path> -d <data_dir> -t <threads>

# 快速模式测试（仅使用前 4096 个字符）
python utils/test_perplexity.py -m <model_path> --quick

# 测试不同嵌入量化类型
python utils/test_perplexity.py -m <model_path> --test-embeddings

# GPU 测试
cd gpu
python test.py

# 端到端基准测试
python utils/e2e_benchmark.py -m <model_path> -n <n_tokens> -p <n_prompt> -t <threads>
```

### 模型转换
```bash
# 从 HuggingFace safetensors 转换为 GGUF
huggingface-cli download microsoft/bitnet-b1.58-2B-4T-bf16 --local-dir ./models/bitnet-b1.58-2B-4T-bf16
python ./utils/convert-helper-bitnet.py ./models/bitnet-b1.58-2B-4T-bf16
```

## 代码风格指南

### Python 代码风格

#### 导入顺序
1. 标准库导入（os, sys, typing 等）
2. 第三方库导入（torch, numpy 等）
3. 本地/项目内部导入（使用相对导入）

```python
import os
import sys
from pathlib import Path
from typing import Optional, Tuple

import torch
import numpy as np

from .module import local_module
```

#### 命名约定
- **变量/函数**: `snake_case`
- **类名**: `PascalCase`
- **常量**: `UPPER_SNAKE_CASE`
- **私有成员**: 单下划线前缀 `_private`
- **避免**: 模糊名称如 `data`, `temp`, `obj`, `item`

#### 类型注解
- 对所有公共 API 使用类型注解
- 使用 `Optional[T]` 表示可空类型
- 使用 `Union[T1, T2]` 或 Python 3.10+ 的 `T1 | T2`

```python
def process_model(
    model_path: Path,
    output_dir: Optional[Path] = None,
    threads: int = 16,
) -> dict:
    """处理模型参数并返回配置字典。"""
    pass
```

#### 函数设计
- 单一职责，目标 ≤ 30 行
- 避免深层嵌套（> 3 层）
- 使用早期返回减少嵌套

#### 错误处理
- 使用明确的异常类型
- 提供有意义的错误消息（包含上下文如 ID、文件名）
- 禁止静默失败

```python
if not model_path.exists():
    raise FileNotFoundError(f"模型文件未找到: {model_path}")
```

#### 注释标准
- 使用 JSDoc/DocString 风格的文档字符串
- 解释 **WHY**（设计决策）和 **HOW**（如果逻辑复杂）
- 模块级、类级和复杂函数需要文档字符串

```python
class ModelConfig:
    """模型配置类，管理量化参数和内核选项。

    职责：
        - 存储模型元数据（维度、层数等）
        - 管理量化类型配置（I2_S, TL1, TL2）
        - 提供验证方法确保配置一致性

    属性:
        dim: 模型隐藏层维度
        n_layers: Transformer 层数
        quant_type: 量化类型（'i2_s', 'tl1', 'tl2'）
    """
    pass
```

### C/C++ 代码风格

#### 命名约定
- **函数**: `snake_case`（如 `ggml_bitnet_init`）
- **变量**: `snake_case`
- **类型/类**: `snake_case` 或 `PascalCase`（与 ggml 风格一致）
- **宏**: `UPPER_SNAKE_CASE`

#### 注释
- C 头文件使用 `//` 单行注释
- 复杂逻辑块添加注释说明设计意图

#### 内存管理
- 使用 RAII 原则（C++）
- 在 C 中显式管理指针生命周期
- 使用初始化检查避免重复初始化（如 `initialized` 标志）

## 代码质量要求

### 模块化
- 高内聚低耦合
- 通过接口抽象外部依赖
- 将单体文件分解为可复用小模块

### 安全
- 硬编码的魔术数字/字符串必须提取到常量/配置
- 绝不硬编码密钥/令牌，使用环境变量
- 验证所有输入（参数、文件路径、API 响应）

### 配置环境
- Dev/Test/Prod 环境隔离
- 无代码嵌入环境逻辑

## 项目结构

```
BitNet-main/
├── src/              # C++ 源代码（内核实现）
├── include/          # C/C++ 头文件
├── gpu/              # GPU 推理和 CUDA 内核
├── utils/            # 实用工具脚本
├── preset_kernels/   # 预调优的内核配置
├── 3rdparty/         # 第三方依赖（llama.cpp）
├── run_inference.py  # 推理入口
├── setup_env.py      # 环境设置脚本
└── CMakeLists.txt    # CMake 构建配置
```

## LSP 配置

项目默认使用 CPU 推理（无需 GPU 依赖）。`gpu/` 模块需要 `torch` 和 `xformers` 依赖：

### 安装 GPU 依赖
```bash
pip install -r gpu/requirements.txt
```

### 修复 LSP 警告
如果看到 `Import "torch/xformers" could not be resolved` 警告：
1. **重启 LSP**：`Ctrl+Shift+P` → `Python: Restart Language Server`
2. **重新加载窗口**：`Ctrl+Shift+P` → `Developer: Reload Window`
3. **选择解释器**：`Ctrl+Shift+P` → `Python: Select Interpreter`

如果不需要 GPU 功能，忽略这些警告（已添加 `# type: ignore` 注释）。

## 测试策略

- 核心逻辑要求高覆盖率（≥ 80%）
- 测试行为而非实现细节
- 使用 `test_perplexity.py` 进行端到端验证
- GPU 测试使用 `gpu/test.py`
