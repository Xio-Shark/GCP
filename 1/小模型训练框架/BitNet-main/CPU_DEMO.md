# CPU 推理完整演示指南

## 前提条件检查

```bash
# Python 版本 >= 3.9
python --version
# 输出示例: Python 3.12.10

# CMake 版本 >= 3.22
cmake --version
# 输出示例: cmake version 4.2.1

# 编译器（Windows: clang/MSVC, Linux/Mac: gcc/clang）
# Windows 需要使用 Visual Studio 2022 的 Developer Command Prompt
```

---

## 完整流程（CPU 推理）

### 第 1 步：安装依赖

```bash
pip install -r requirements.txt
```

主要依赖包括：
- `numpy` - 数值计算
- `transformers` - HuggingFace 模型处理
- `huggingface_hub` - 模型下载
- `gguf` - GGUF 格式支持

---

### 第 2 步：构建项目

#### Windows（Visual Studio 2022 + Clang）

在 **Developer Command Prompt for VS2022** 中执行：

```bash
cd BitNet

# 设置环境并构建（自动处理 CMake + 模型准备）
python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s
```

#### Linux/Mac

```bash
cd BitNet
python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s
```

**setup_env.py 执行内容：**
1. 安装 gguf-py 依赖
2. 根据模型生成内核代码（codegen_tl1.py / codegen_tl2.py）
3. 运行 CMake 构建
4. 从 HuggingFace 下载模型
5. 转换为 GGUF 格式（I2_S 量化）
6. 可选：量化嵌入为 f16（`--quant-embd`）

---

### 第 3 步：运行推理

#### 基本对话模式

```bash
python run_inference.py \
  -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  -p "你是一个有用的助手" \
  -cnv \
  -t 4 \
  -n 128 \
  -temp 0.8
```

**交互式对话示例：**

```
你: 北京今天天气怎么样？
BitNet: 我是一个 AI 助手，无法提供实时天气信息，建议您查看天气预报应用。
```

#### 单轮推理（非对话模式）

```bash
python run_inference.py \
  -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  -p "人工智能的未来发展趋势是什么？" \
  -t 4 \
  -n 256
```

#### 启动推理服务器

```bash
python run_inference_server.py
```

然后使用 HTTP API 调用：

```bash
curl http://localhost:5001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "bitnet-2b",
    "messages": [{"role": "user", "content": "你好"}],
    "max_tokens": 128
  }'
```

---

### 第 4 步：测试和基准测试

#### 困惑度测试

```bash
# 快速测试（前 4096 字符）
python utils/test_perplexity.py \
  -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  --quick

# 完整测试（所有数据集）
python utils/test_perplexity.py \
  -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  -d data \
  -t 16

# 测试不同嵌入量化类型
python utils/test_perplexity.py \
  -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  --test-embeddings
```

#### 端到端性能测试

```bash
python utils/e2e_benchmark.py \
  -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  -n 128 \
  -p 256 \
  -t 4
```

---

## 支持的 CPU 内核类型

| 架构 | 内核类型 | 说明 | 设置参数 |
|------|----------|------|----------|
| ARM64 | `i2_s` | 通用量化 | `-q i2_s` |
| ARM64 | `tl1` | LUT 查找表优化 | `-q tl1` |
| x86_64 | `i2_s` | 通用量化 | `-q i2_s` |
| x86_64 | `tl2` | LUT 查找表优化（推荐） | `-q tl2` |

---

## 使用其他模型

### 从 HuggingFace 下载并转换

```bash
# 方法 1：使用 setup_env.py（推荐）
python setup_env.py -hr 1bitLLM/bitnet_b1_58-3B -q i2_s

# 方法 2：手动下载并转换
# 下载模型
huggingface-cli download microsoft/bitnet-b1.58-2B-4T-bf16 --local-dir ./models/bitnet-b1.58-2B-4T-bf16

# 转换为 GGUF
python utils/convert-helper-bitnet.py ./models/bitnet-b1.58-2B-4T-bf16
```

### 支持的官方模型

| 模型 | 参数 | 下载命令 |
|------|------|----------|
| BitNet-b1.58-2B-4T | 2.4B | `python setup_env.py -hr microsoft/BitNet-b1.58-2B-4T -q i2_s` |
| bitnet_b1_58-3B | 3.3B | `python setup_env.py -hr 1bitLLM/bitnet_b1_58-3B -q i2_s` |
| Falcon3-7B-1.58bit | 7B | `python setup_env.py -hr tiiuae/Falcon3-7B-Instruct-1.58bit -q i2_s` |

---

## 常见问题

### Q1: 构建失败 "cmake: command not found"

```bash
# Windows: 安装 CMake 并添加到 PATH
# Linux/Mac:
sudo apt-get install cmake  # Ubuntu/Debian
brew install cmake         # macOS
```

### Q2: 编译器错误

```bash
# Windows: 确保 clang 已安装并在 PATH 中
choco install llvm

# 或使用 Visual Studio 2022（推荐），在 Developer Command Prompt 中运行
```

### Q3: 推理缓慢

- 增加 `-t` 参数（线程数）：`-t 8` 或 `-t 16`
- 使用优化的内核类型：x86 用 `-q tl2`，ARM 用 `-q tl1`
- 减小上下文大小：`-c 2048`（默认）

### Q4: 内存不足

- 减小线程数：`-t 2`
- 使用较小的模型（如 bitnet_b1_58-large）

---

## 性能参考（CPU）

| 模型 | 架构 | 内核 | tokens/s | 能耗节省 |
|------|------|------|----------|----------|
| BitNet-b1.58-2B-4T | ARM64 | TL1 | 5-7 | 55% |
| BitNet-b1.58-2B-4T | x86_64 | TL2 | 5-7 | 70% |

---

## 总结

CPU 推理完整流程：

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 设置环境并自动构建
python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s

# 3. 运行推理
python run_inference.py -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  -p "你是一个有用的助手" -cnv -t 4 -n 128
```

**关键参数：**
- `-q i2_s`：通用量化（兼容所有架构）
- `-q tl1`：ARM 优化内核
- `-q tl2`：x86 优化内核（推荐）
- `-t 4`：使用 4 个线程（建议根据 CPU 核心数调整）
- `--quant-embd`：量化嵌入减小模型体积（可选）
