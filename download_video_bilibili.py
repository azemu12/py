import os
import time
import random
import json
import yt_dlp
from loguru import logger


def download_video(dirs, file_name, file_url,cookie_path):
    def _run_download(use_cookies=False):
        ydl_opts_download = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(dirs, file_name),
            # 'proxy': proxy,
            'merge_output_format': 'mp4',
            'quiet': True,
            'verbose': True,
            'retries': 5,
            'continuedl': True,
            'concurrent_fragment_downloads': 10,  # 多分片并行
            'noprogress': False,  # 显示进度
        }

        if use_cookies:
            ydl_opts_download['cookies'] = cookie_path
            logger.info(f"⚠️ 使用 Cookie 文件重试下载: {file_name}")

        with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
            ydl.download([file_url])

    try:
        # 第一次尝试，不使用 cookie
        _run_download(use_cookies=False)
        logger.info(f"{file_name} 下载成功 ✅（无 Cookie）")
        return 1

    except Exception as e1:
        logger.info(f"{file_name} 第一次下载失败 ❌，错误：{e1}")
        time.sleep(random.randint(1, 3))

        try:
            # 第二次尝试，使用 cookie
            _run_download(use_cookies=True)
            logger.info(f"{file_name} 下载成功 ✅（使用 Cookie）")
            return 1

        except Exception as e2:
            logger.info(f"{file_name} 下载失败 ❌（使用 Cookie 后仍失败），错误：{e2}")
            return -1

if __name__ == '__main__':
    dirs = r'/sdc1/mada_16t/download_bilibili_1209_2'
    with open("video_href_2.json", "r",encoding="utf-8") as f:
        lines = [json.loads(line) for line in f]   # 读一次
    for video_item in lines[-10:]:
    
        video_url = video_item["video_href"]
        file_name = f"{video_item['index']}.mp4"
        if os.path.exists(os.path.join(dirs, file_name)):
            logger.info(f"{file_name} 已存在，跳过下载")
            continue
        download_video(dirs, file_name, video_url, "1.txt")



