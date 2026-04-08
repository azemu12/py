import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# ===== 配置区 =====
ROOT_DIR = r"G:\youtube_data\Youtube_01"       # 原视频根目录
TARGET_DIR = r"G:\youtube_data\Youtube_01_good"# 目标目录（复刻结构）
MIN_SIZE = 1080                  # 最小宽或高
DRY_RUN = True                   # True=只打印不移动，确认无误后改 False
MAX_WORKERS = 8                  # 线程数

VIDEO_EXTS = {
    ".mp4", ".mov", ".mkv", ".avi",
    ".flv", ".wmv", ".webm", ".m4v"
}


# ================= 获取视频分辨率 =================
def get_video_resolution(video_path: Path):
    """
    使用 ffprobe 获取宽高
    返回: (width, height) 或 (None, None)
    """
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "csv=p=0:s=x",
        str(video_path)
    ]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15
        )

        if result.returncode != 0:
            return None, None

        text = result.stdout.strip()
        if "x" not in text:
            return None, None

        w, h = text.split("x")
        return int(w), int(h)

    except Exception:
        return None, None


# ================= 处理单个视频 =================
def process_video(video_path: Path):
    width, height = get_video_resolution(video_path)

    if width is None or height is None:
        print(f"[跳过] 无法解析: {video_path}")
        return

    # 核心修改：计算文件相对于根目录的相对路径，保留文件夹结构
    rel_path = video_path.relative_to(ROOT_DIR)
    target_path = Path(TARGET_DIR) / rel_path

    if width >= MIN_SIZE and height >= MIN_SIZE:
        print(f"[移动] {video_path}  ({width}x{height}) -> {target_path}")

        if not DRY_RUN:
            try:
                # 创建目标文件夹（自动复刻层级）
                target_path.parent.mkdir(parents=True, exist_ok=True)
                # 移动文件
                video_path.rename(target_path)
            except Exception as e:
                print(f"[移动失败] {video_path} -> {e}")
    else:
        print(f"[保留] {video_path}  ({width}x{height})")


# ================= 收集视频 =================
def collect_videos(root: Path):
    videos = []
    for path in root.rglob("*"):
        if path.suffix.lower() in VIDEO_EXTS:
            videos.append(path)
    return videos


# ================= 主函数 =================
def main():
    root = Path(ROOT_DIR)
    target = Path(TARGET_DIR)

    if not root.exists():
        print("❌ 根目录不存在")
        return

    # 确保目标目录存在
    if not target.exists():
        print(f"📁 创建目标目录: {target}")
        if not DRY_RUN:
            target.mkdir(parents=True, exist_ok=True)

    print("🔍 扫描视频中...")
    videos = collect_videos(root)
    print(f"🎬 共发现 {len(videos)} 个视频")

    print("⚙️ 开始处理...")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = [ex.submit(process_video, v) for v in videos]
        for _ in as_completed(futures):
            pass

    print("✅ 完成")


if __name__ == "__main__":
    main()