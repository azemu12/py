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

def download_media(save_path, video_addr,download_work_max_retry):
    if os.path.exists(save_path + '.mp4'):
        logger.info(f'文件已存在: {save_path + ".mp4"}')
        return
    headers = HeaderBuilder().build(HeaderType.GET)
    headers.set_referer(video_addr)
    for retry_count in range(download_work_max_retry):
        try:
            r = curl_requests.get(video_addr, headers=headers.get(), stream=True, timeout=30)
            if r.status_code == 200:
                # 获取文件总大小（如果响应头里提供了）
                total_size = int(r.headers.get('Content-Length', 0))
                block_size = 8192  # 每次写入的字节数

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
                return True  # 下载成功
            else:
                logger.error(f"{video_addr} 请求失败: {r.status_code}")
                
        except Exception as e:
            logger.error(f"{video_addr} 下载失败: {str(e)}")
        
        if retry_count < download_work_max_retry - 1:
            delay = 1 * (2 ** retry_count)  # 指数退避
            logger.info(f"{video_addr} 等待 {delay} 秒后重试... ({retry_count + 1}/{download_work_max_retry})")
            time.sleep(delay)

    logger.error(f"{video_addr} 达到最大重试次数 {max_retry}，下载失败")
    return False

def download_work(work_info,download_work_max_retry):
    save_path = work_info["save_path"]
    check_and_create_path(os.path.dirname(save_path))
    logger.info(f'正在下载视频链接 {work_info["video_addr"]}')
    download_media(save_path, work_info['video_addr'],download_work_max_retry)
    logger.info(f'作品 {work_info["aweme_id"]} 下载完成，保存路径: {save_path}')
    return save_path


# 检查创建文件夹
def check_and_create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
