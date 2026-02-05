import os
import json
import pandas as pd
from pathlib import Path


def convert_conversation_to_messages(conversations, system_prompt="You are a helpful, respectful and honest assistant."):
    """
    将 conversations 列表转换为 messages 格式
    """
    messages = []
    
    # 添加 system message
    messages.append({
        "role": "system",
        "content": system_prompt
    })
    
    # 转换 conversation entries
    for conv in conversations:
        from_field = conv.get('from', '').lower()
        value = conv.get('value', '')
        
        # 映射 from 字段到 role
        if from_field in ['human', 'user']:
            role = 'user'
        elif from_field in ['assistant', 'gpt']:
            role = 'assistant'
        else:
            # 默认映射
            role = from_field
        
        messages.append({
            "role": role,
            "content": value
        })
    
    return messages


def process_parquet_file(parquet_path):
    """
    读取单个 parquet 文件并转换为目标格式
    """
    df = pd.read_parquet(parquet_path)
    
    results = []
    for _, row in df.iterrows():
        conversations = row.get('conversations', [])
        item_id = row.get('id', '')
        
        # 转换为 messages 格式
        messages = convert_conversation_to_messages(conversations)
        
        result_item = {
            "messages": messages
        }
        
        # 可选：保留原始 id
        if item_id:
            result_item["id"] = item_id
        
        results.append(result_item)
    
    return results


def main():
    # 配置
    input_dir = Path(__file__).parent  # AgentInstruct 文件夹
    output_file = input_dir / "agent_instruct_converted.json"
    
    # 查找所有 parquet 文件
    parquet_files = list(input_dir.glob("*.parquet"))
    
    if not parquet_files:
        print(f"在 {input_dir} 中未找到 parquet 文件")
        return
    
    print(f"找到 {len(parquet_files)} 个 parquet 文件:")
    for f in parquet_files:
        print(f"  - {f.name}")
    
    # 处理所有 parquet 文件
    all_data = []
    for parquet_path in sorted(parquet_files):
        print(f"\n正在处理: {parquet_path.name} ...")
        try:
            data = process_parquet_file(parquet_path)
            all_data.extend(data)
            print(f"  ✓ 转换了 {len(data)} 条记录")
        except Exception as e:
            print(f"  ✗ 错误: {e}")
    
    # 保存为 JSON
    print(f"\n总计转换了 {len(all_data)} 条记录")
    print(f"正在保存到: {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    print("✓ 完成!")


if __name__ == "__main__":
    main()
