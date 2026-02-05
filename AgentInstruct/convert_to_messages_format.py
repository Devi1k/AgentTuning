import json

# 配置路径
input_file = "my_reproduction_general_data.json"
output_file = "my_reproduction_general_data_converted.json"

# 默认系统消息
SYSTEM_MESSAGE = "You are a helpful assistant."

# 加载数据
print(f"正在加载 {input_file} ...")
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"原始数据总量: {len(data)}")

# 转换格式
converted_data = []

for item in data:
    # 创建新的 messages 格式
    messages_item = {
        "messages": []
    }
    
    # 添加 system message
    messages_item["messages"].append({
        "role": "system",
        "content": SYSTEM_MESSAGE
    })
    
    # 转换 conversations 为 messages
    for conv in item.get("conversations", []):
        role = conv.get("from", "")
        content = conv.get("value", "")
        
        # 映射角色
        if role == "human":
            mapped_role = "user"
        elif role == "gpt":
            mapped_role = "assistant"
        else:
            mapped_role = role  # 保留其他角色
        
        messages_item["messages"].append({
            "role": mapped_role,
            "content": content
        })
    
    converted_data.append(messages_item)

# 保存结果
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(converted_data, f, indent=2, ensure_ascii=False)

print(f"成功！已转换 {len(converted_data)} 条数据到 {output_file}")
print(f"格式示例: {{'messages': [{{'role': 'system', 'content': '...'}}, {{'role': 'user', 'content': '...'}}, {{'role': 'assistant', 'content': '...'}}]}}")
