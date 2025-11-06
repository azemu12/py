import os
import json
import pandas as pd

date_time = '20251105'
excel_path = '1P_250319 全身视频采集_抖音号1082_链接671.xlsx'
sheet_name = '抖音号-1082'

# === 没有表头，header=None ===
data = pd.read_excel(excel_path, sheet_name=sheet_name, header=None)

# 假设第 1 列（索引 0）是抖音号
user_id_list = data.iloc[:, 0].astype(str).tolist()

# ========== 自动延续 index ==========
json_dir = 'json'
os.makedirs(json_dir, exist_ok=True)

# 查找 json 目录下的所有 json 文件
existing_files = [f for f in os.listdir(json_dir) if f.endswith('user_id_list.json')]

max_index = 0
for file in existing_files:
    file_path = os.path.join(json_dir, file)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list) and len(data) > 0 and 'id' in data[-1]:
                # 从最后一条的 id 提取数字部分
                last_id = int(data[-1]['id'])
                if last_id > max_index:
                    max_index = last_id
    except Exception as e:
        print(f"⚠️ 读取 {file} 失败: {e}")

# 新的 index 从上次的最大值 + 1 开始
index = max_index + 1

# ========== 写入新 JSON ==========
results_list = []
for user_id in user_id_list:
    results_list.append({
        'id': f'{index:08d}',
        'user_id': user_id,
        'date_time': date_time
    })
    index += 1

output_path = os.path.join(json_dir, f'{date_time}_user_id_list.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results_list, f, ensure_ascii=False, indent=4)

print(f"✅ 成功生成 {output_path}")
print(f"📦 本次起始 index: {max_index + 1}, 结束 index: {index - 1}")
