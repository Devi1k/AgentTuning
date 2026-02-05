## ReWOO 任务测评运行指南

ReWOO 是另一个 held-out 测评任务，以下是运行方法：

### 1. 环境准备

进入 rewoo 目录并安装依赖：

```bash
cd eval_heldout/rewoo
pip install -r requirements.txt
```

主要依赖包括：
- `langchain==0.0.187`
- `openai==0.27.4`
- `fschat` (用于连接本地模型)
- `wikipedia`, `google-search-results` (工具依赖)

### 2. 配置 API Keys

创建 `keys` 目录并添加 API keys：

```bash
mkdir -p keys
echo "your-openai-key" > keys/openai.key
echo "your-serper-key" > keys/serper.key
echo "your-wolfram-key" > keys/wolfram.key
```

**注意**：即使使用本地模型，也需要提供 OpenAI key，因为 evaluator 依赖它进行评分。

### 3. 启动模型服务

ReWOO 使用 FastChat 的 TGI 接口。首先需要启动模型服务：

```bash
# 使用 docker 启动 TGI 服务（端口 30007）
cd docker
docker compose -f agentlm-7b.yml up
```

然后设置环境变量指向服务地址：

```bash
export CONTROLLER_ADDR=http://127.0.0.1:30007
```

### 4. 运行测评

#### 方式一：使用提供的脚本（推荐）

```bash
# 测评所有任务
bash eval-tgi.sh
```

#### 方式二：手动运行单个任务

```bash
python run_eval.py \
    --method rewoo \
    --dataset hotpot_qa \
    --sample_size 50 \
    --toolset Wikipedia LLM \
    --base_lm agent-llama \
    --save_result
```

### 支持的参数

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `--method` | 测评方法 | `direct`, `cot`, `react`, `rewoo` |
| `--dataset` | 数据集 | `hotpot_qa`, `trivia_qa`, `gsm8k`, `physics_question`, `sports_understanding`, `strategy_qa`, `sotu_qa` |
| `--sample_size` | 测评样本数 | 默认 10 |
| `--toolset` | 可用工具 | `Google`, `Wikipedia`, `WolframAlpha`, `Calculator`, `LLM` |
| `--base_lm` | 基础模型 | `agent-llama`, `gpt-3.5-turbo`, `gpt-4` 等 |
| `--planner_lm` | Planner 模型 | 默认为 base_lm |
| `--solver_lm` | Solver 模型 | 默认为 base_lm |

### 各数据集推荐工具配置

| 数据集 | 推荐工具 |
|--------|----------|
| hotpot_qa | Wikipedia, LLM |
| trivia_qa | Wikipedia, LLM |
| gsm8k | LLM, WolframAlpha, Calculator |
| strategy_qa | Wikipedia, LLM, WolframAlpha, Calculator, Google |
| physics_question | Wikipedia, LLM, WolframAlpha, Calculator, Google |
| sports_understanding | Wikipedia, LLM, WolframAlpha, Calculator, Google |
| sotu_qa | LLM, Calculator, Google, SearchSOTU |

### 5. 查看结果

测评结果会保存在：
- 日志文件：`logs/`, `results/` 目录
- CSV 结果：`results/eval_{dataset}_{method}_{model}.csv`

运行以下命令计算指标：

```bash
python metrics.py
```

### 与 HotpotQA 的区别

| 特性 | HotpotQA | ReWOO |
|------|----------|-------|
| 模型连接 | 直接连接 TGI | 通过 FastChat 连接 |
| 环境变量 | `--ip`, `--port` 参数 | `CONTROLLER_ADDR` |
| 测评方法 | React Agent | direct/cot/react/rewoo |
| 数据集 | HotpotQA 三个难度 | 7 个不同数据集 |
| 工具使用 | 内置 Wikipedia | 可配置多种工具 |