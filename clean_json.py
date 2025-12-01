import json

# 输入文件
progress_file = "progress.json"
fail_file = "fail.json"

# 输出文件
output_file = "finished_clean.json"

# 读取 progress.json
with open(progress_file, "r", encoding="utf-8") as f:
    progress_data = json.load(f)

# 读取 fail.json
with open(fail_file, "r", encoding="utf-8") as f:
    fail_data = json.load(f)

finished_list = progress_data.get("finished", [])
failed_list = fail_data.get("failed", [])

# 转成 set 进行快速度去重过滤
failed_set = set(failed_list)

# 去除出现在 failed 里的元素
clean_finished = [x for x in finished_list if x not in failed_set]

# 保存输出
with open(output_file, "w", encoding="utf-8") as f:
    json.dump({"finished": clean_finished}, f, ensure_ascii=False, indent=4)

print("去重后的 finished 已生成 → finished_clean.json")
