import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = "/sdc1/mada_16t/download_1112"
DRY_RUN =  False     # True = 模拟删除 / False = 真删除
MAX_WORKERS = 32     # 并发线程数，根据 CPU 核心调整

def get_duration(path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", path
    ]
    try:
        result = subprocess.check_output(cmd).decode().strip()
        return float(result)
    except:
        return 0

def process_file(path):
    duration = get_duration(path)
    if duration > 91:
        if DRY_RUN:
            return f"[模拟] 将删除: {path} （时长: {duration:.1f} 秒）"
        else:
            os.remove(path)
            return f"[删除] {path} （时长: {duration:.1f} 秒）"
    return None

# 收集所有 mp4 文件
files = []
for root, dirs, fs in os.walk(ROOT):
    for f in fs:
        if f.lower().endswith(".mp4"):
            files.append(os.path.join(root, f))

print(f"共发现 {len(files)} 个 mp4 文件，开始并发处理…")

# 多线程处理
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {executor.submit(process_file, f): f for f in files}

    for future in as_completed(futures):
        msg = future.result()
        if msg:
            print(msg)
