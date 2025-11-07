import json
import os
import re
import time
import openpyxl
import requests
from loguru import logger
from retry import retry
from curl_cffi import requests as curl_requests
from tqdm import tqdm
from builder.header import HeaderBuilder, HeaderType
CACHE_FILE = "download_cache.json"

def norm_str(str):
    new_str = re.sub(r"|[\\/:*?\"<>| ]+", "", str).replace('\n', '').replace('\r', '')
    return new_str

def norm_text(text):
    ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
    text = ILLEGAL_CHARACTERS_RE.sub(r'', text)
    return text


def timestamp_to_str(timestamp):
    time_local = time.localtime(timestamp / 1000)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt

def load_download_cache():
    """读取下载缓存"""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f).get("downloaded", []))
    return set()

def save_download_cache(downloaded_set):
    """保存下载缓存"""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({"downloaded": list(downloaded_set)}, f, ensure_ascii=False, indent=2)
        
def download_media(save_path, video_addr, work_id, download_work_max_retry):
    """
    根据 video_addr 下载视频
    使用 work_id 去重
    """
    downloaded_set = load_download_cache()

    # ✅ 如果该作品已下载过，无论在哪个路径都跳过
    if work_id in downloaded_set:
        logger.info(f"作品 {work_id} 已下载过，跳过")
        return True

    headers = HeaderBuilder().build(HeaderType.GET)
    headers.set_referer(video_addr)

    for retry_count in range(download_work_max_retry):
        try:
            r = curl_requests.get(video_addr, headers=headers.get(), stream=True, timeout=30)
            if r.status_code == 200:
                total_size = int(r.headers.get('Content-Length', 0))
                block_size = 8192

                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                with open(save_path + '.mp4', "wb") as f, tqdm(
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    desc=f"下载中 (尝试 {retry_count + 1}/{download_work_max_retry})",
                    ncols=80
                ) as bar:
                    for chunk in r.iter_content(chunk_size=block_size):
                        if chunk:
                            f.write(chunk)
                            bar.update(len(chunk))

                # ✅ 下载成功 -> 写入缓存
                downloaded_set.add(work_id)
                save_download_cache(downloaded_set)
                logger.success(f"✅ 下载完成: {work_id}")
                return True

            else:
                logger.error(f"{video_addr} 请求失败: {r.status_code}")

        except Exception as e:
            logger.error(f"{video_addr} 下载失败: {str(e)}")

        if retry_count < download_work_max_retry - 1:
            delay = 1 * (2 * retry_count)
            logger.info(f"{video_addr} 等待 {delay} 秒后重试... ({retry_count + 1}/{download_work_max_retry})")
            time.sleep(delay)

    logger.error(f"{video_addr} 达到最大重试次数 {download_work_max_retry}，下载失败")
    return False

def download_media_one(save_path, video_addr, work_id, download_work_max_retry):
    """
    根据 video_addr 下载视频
    使用 work_id 去重
    """

    headers = HeaderBuilder().build(HeaderType.GET)
    headers.set_referer(video_addr)

    for retry_count in range(download_work_max_retry):
        try:
            r = curl_requests.get(video_addr, headers=headers.get(), stream=True, timeout=30)
            if r.status_code == 200:
                total_size = int(r.headers.get('Content-Length', 0))
                block_size = 8192

                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                with open(save_path + '.mp4', "wb") as f, tqdm(
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    desc=f"下载中 (尝试 {retry_count + 1}/{download_work_max_retry})",
                    ncols=80
                ) as bar:
                    for chunk in r.iter_content(chunk_size=block_size):
                        if chunk:
                            f.write(chunk)
                            bar.update(len(chunk))
                logger.success(f"✅ 下载完成: {work_id}")
                return True

            else:
                logger.error(f"{video_addr} 请求失败: {r.status_code}")

        except Exception as e:
            logger.error(f"{video_addr} 下载失败: {str(e)}")

        if retry_count < download_work_max_retry - 1:
            delay = 1 * (2 * retry_count)
            logger.info(f"{video_addr} 等待 {delay} 秒后重试... ({retry_count + 1}/{download_work_max_retry})")
            time.sleep(delay)

    logger.error(f"{video_addr} 达到最大重试次数 {download_work_max_retry}，下载失败")
    return False

def download_work(work_info,download_work_max_retry,download_type):
    save_path = work_info["save_path"]
    check_and_create_path(os.path.dirname(save_path))
    logger.info(f'正在下载视频链接 {work_info["video_addr"]}')
    if download_type == "one":
        success = download_media_one(save_path, work_info['video_addr'], work_info['aweme_id'], download_work_max_retry)
    elif download_type == "all":
        success = download_media(save_path, work_info['video_addr'], work_info['aweme_id'], download_work_max_retry)
    if success:
        logger.info(f'作品 {work_info["aweme_id"]} 下载完成，保存路径: {save_path}')
    else:
        logger.error(f'作品 {work_info["aweme_id"]} 下载失败，保存路径: {save_path}')
    return save_path


# 检查创建文件夹
def check_and_create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
