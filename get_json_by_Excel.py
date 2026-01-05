import json
import pandas as pd

# 1. 读取 Excel 文件
# 修改成你的文件名，例如：data.xlsx
excel_path = r"/home/gct/DY/data/0105_15P_单人全身视频抖音号链接_抖音号5605个+视频链接360个_0104.xlsx"

# 默认读取第一张表，也可以指定 sheet_name="抖音号366"
df = pd.read_excel(excel_path, header=None)

# 2. 取第一列作为 user_id 列
user_ids = df.iloc[:, 0].astype(str).str.replace(r'[\n\r"]', '', regex=True)

# 3. 转换为 JSON 数组，id 从 0 开始
result = []

for i, uid in enumerate(user_ids):
    result.append({
        "id": i,           # 从0开始
        "user_id": uid,    # Excel内容
        "date_time": "20260105"  # 可按需修改
    })

# 4. 保存到 JSON 文件
with open("20260105_user_id_list.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("转换完成 → 20260105_user_id_list.json")  