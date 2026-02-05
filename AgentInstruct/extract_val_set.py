import json
import random

def extract_val_set(input_file, output_file, num_samples=200, seed=42):
    """
    从原始数据集中抽取指定数量的样本作为验证集
    
    Args:
        input_file: 输入的 JSON 文件路径
        output_file: 输出的验证集文件路径
        num_samples: 抽取的样本数量
        seed: 随机种子，保证可复现
    """
    # 读取原始数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"原始数据集总条数: {len(data)}")
    
    # 设置随机种子以保证可复现
    random.seed(seed)
    
    # 随机抽取样本
    if len(data) <= num_samples:
        val_set = data
        print(f"数据集总条数 ({len(data)}) 小于等于需要抽取的条数 ({num_samples})，使用全部数据")
    else:
        val_set = random.sample(data, num_samples)
    
    # 保存验证集
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(val_set, f, ensure_ascii=False, indent=2)
    
    print(f"验证集已保存到: {output_file}")
    print(f"验证集条数: {len(val_set)}")
    
    # 打印验证集的基本信息
    if val_set:
        print(f"\n验证集第一条数据示例:")
        print(f"  ID: {val_set[0].get('id', 'N/A')}")
        print(f"  Messages 数量: {len(val_set[0].get('messages', []))}")
    
    return val_set

if __name__ == "__main__":
    input_file = "D:\\ft\AgentTuning\\AgentInstruct\\agent_instruct_converted.json"
    output_file = "val_set_200.json"
    
    extract_val_set(input_file, output_file, num_samples=200, seed=42)
