import json
import random
# 需要安装: pip install langdetect
from langdetect import detect, LangDetectException
import tqdm

# 1. 配置路径
input_file = "AgentInstruct\\ShareGPT_V3_unfiltered_cleaned_split.json"
output_file = "my_reproduction_general_data.json"
TARGET_COUNT = 4532  # 根据之前计算得到的 N_general

# 2. 加载数据
print(f"正在加载 {input_file} ...")
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"原始数据总量: {len(data)}")

# 3. 英语过滤 & 基础清洗
english_conversations = []

print("正在过滤非英语对话 (这可能需要几分钟)...")
for conv in tqdm.tqdm(data):
    # ShareGPT 的格式通常是 [{"from": "human", "value": "..."}]
    # 我们通常检测第一句或第二句来判断语言
    try:
        # 拼接前几句话来检测语言，提高准确率
        sample_text = ""
        if len(conv['conversations']) > 0:
            sample_text += conv['conversations'][0]['value']
        if len(conv['conversations']) > 1:
            sample_text += " " + conv['conversations'][1]['value']
            
        if not sample_text.strip():
            continue
            
        # 检测语言
        if detect(sample_text) == 'en':
            # 论文中还提到了 GPT-4 和 GPT-3.5 的区分
            # 注意：在该数据集中，模型信息往往丢失或不标准。
            # 如果 conv 中包含 'model' 字段可以利用，如果没有，只能作为通用池处理。
            english_conversations.append(conv)
            
    except LangDetectException:
        continue
    except KeyError:
        continue

print(f"英语对话数量: {len(english_conversations)}")

# 4. 解决 GPT-4 vs GPT-3.5 的问题
# 现实情况：这个 json 文件里很多数据没有标记 model 版本。
# 论文作者可能有原始 meta data。
# 复现时的工程妥协：由于你需要的数据量 (4.5k) 远小于英语池子 (可能 40k+)，
# 且 ShareGPT 里的长对话质量通常较高。我们采用【随机采样】。
# 只要数据是 ShareGPT 的，它就代表了 "General Domain"。

if len(english_conversations) < TARGET_COUNT:
    print(f"警告：英语数据不足 {TARGET_COUNT} 条！使用了全部可用数据。")
    selected_data = english_conversations
else:
    print(f"正在随机采样 {TARGET_COUNT} 条数据...")
    selected_data = random.sample(english_conversations, TARGET_COUNT)

# 5. 保存结果
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(selected_data, f, indent=2, ensure_ascii=False)

print(f"成功！已保存 {len(selected_data)} 条数据到 {output_file}")
print("接下来请将此数据与你的 Agent 数据混合。")
