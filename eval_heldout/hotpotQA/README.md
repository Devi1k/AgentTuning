根据代码分析，以下是如何运行 HotpotQA 测评的完整步骤：

## HotpotQA 测评运行指南

### 1. 环境准备

首先进入 hotpotQA 目录并安装依赖：

```bash
cd eval_heldout/hotpotQA
pip install -r requirements.txt
```

依赖包括：
- `langchain==0.0.174`
- `pandas<=2.0.0`

### 2. 启动模型服务

使用 Text-Generation-Inference (TGI) 启动模型。以 AgentLM-7B 为例：

```bash
cd docker
docker compose -f agentlm-7b.yml up
```

这会启动一个推理服务，默认端口为 `30007`。

### 3. 运行测评脚本

回到 `eval_heldout/hotpotQA` 目录，执行：

```bash
python eval_hotpot.py \
    --agent_name React_HotPotQA_run_Agent \
    --llm_name agentlm-7b \
    --ip 127.0.0.1 \
    --port 30007 \
    --max_context_len 1700
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--agent_name` | Agent 架构类型 | `React` |
| `--llm_name` | 模型名称 | `gpt-3.5-turbo` |
| `--ip` | TGI 服务 IP | `127.0.0.1` |
| `--port` | TGI 服务端口 | `23333` |
| `--min` | 端口范围最小值 | `23330` |
| `--max` | 端口范围最大值 | `23337` |
| `--max_context_len` | 最大上下文长度 | `1700` |

### 支持的 Agent 类型

在 [`src/config.py`](eval_heldout/hotpotQA/src/config.py:8) 中定义了以下可用 agent：
- `Zeroshot_HotPotQA_run_Agent`
- `ZeroshotThink_HotPotQA_run_Agent`
- `React_HotPotQA_run_Agent`
- `Planner_HotPotQA_run_Agent`
- `PlannerReact_HotPotQA_run_Agent`

### 测评数据

HotpotQA 测评包含三个难度级别：
- `easy` - 简单问题
- `medium` - 中等难度
- `hard` - 困难问题

数据文件位于 [`src/data/`](eval_heldout/hotpotQA/src/data/) 目录下。

### 输出结果

测评结果会保存在：
- 执行日志：`execution_data/{port_min}-{port_max}/{level}_{agent_name}_{llm_name}.jsonl`
- 汇总结果：`result_{timestamp}.json`

结果包含每个难度级别的平均得分以及总体平均分。