import os

ROOT = "/sdc1/mada_16t/download_1112"
KEEP = 20
DRY_RUN = False  # True = 模拟删除；False = 真删除

for dirpath, dirnames, filenames in os.walk(ROOT):
    # 只处理每个文件夹内的 mp4 文件
    mp4_files = sorted([f for f in filenames if f.lower().endswith(".mp4")])

    if len(mp4_files) <= KEEP:
        continue  # 不需要处理

    # 要删除的文件
    to_delete = mp4_files[KEEP:]

    for f in to_delete:
        full = os.path.join(dirpath, f)
        if DRY_RUN:
            print(f"[模拟] 将删除: {full}")
        else:
            print(f"[删除] {full}")
            os.remove(full)
