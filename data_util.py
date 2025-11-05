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

def download_media(path, name, url, type,work_url):
    if os.path.exists(path + '.mp4'):
        logger.info(f'文件已存在: {path + ".mp4"}')
        return
    headers = HeaderBuilder().build(HeaderType.GET)
    headers.set_referer(work_url)
    if type == 'image':
        content = requests.get(url,headers=headers.get()).content
        # with open(path + '/' + name + '.jpg', mode="wb") as f:
        with open(path + '.jpg', mode="wb") as f:
            f.write(content)
            f.close()
    elif type == 'video':
        # res = requests.get(url, stream=True,headers=headers)
        # size = 0
        # chunk_size = 1024 * 1024
        # # with open(path + '/' + name + '.mp4', mode="wb") as f:
        # with open(path + '.mp4', mode="wb") as f:
        #     for data in res.iter_content(chunk_size=chunk_size):
        #         f.write(data)
        #         size += len(data)
        for retry_count in range(5):
            try:
                r = curl_requests.get(url, headers=headers.get(), stream=True, timeout=30)
                
                if r.status_code == 200:
                    # 获取文件总大小（如果响应头里提供了）
                    total_size = int(r.headers.get('Content-Length', 0))
                    block_size = 8192  # 每次写入的字节数
    
                    with open(path + '.mp4', "wb") as f, tqdm(
                        total=total_size,
                        unit='B',
                        unit_scale=True,
                        unit_divisor=1024,
                        desc=f"下载中 (尝试 {retry_count + 1}/{5})",
                        ncols=80
                    ) as bar:
                        for chunk in r.iter_content(chunk_size=block_size):
                            if chunk:
                                f.write(chunk)
                                bar.update(len(chunk))
                    return True  # 下载成功
                else:
                    print(f"请求失败: {r.status_code}")
                    
            except (curl_requests.RequestException, ConnectionError) as e:
                print(f"下载失败: {str(e)}")
            
            if retry_count < 5 - 1:
                delay = 1 * (2 ** retry_count)  # 指数退避
                print(f"等待 {delay} 秒后重试... ({retry_count + 1}/{5})")
                time.sleep(delay)
    
        print(f"达到最大重试次数 {5}，下载失败")
        return False



def download_work(work_info, path, save_choice):
    work_id = work_info['work_id']
    save_path = f'{work_info["save_path"]}/{work_id}'

    check_and_create_path(os.path.dirname(save_path))

    work_type = work_info['work_type']
    logger.info(f'正在下载作品 {work_id} 类型 {work_type}')
    if work_type == '视频':
        logger.info(f'正在下载视频链接 {work_info["video_addr"]}')
        download_media(save_path, 'video', work_info['video_addr'], 'video',work_info["work_url"])
    logger.info(f'作品 {work_info["work_id"]} 下载完成，保存路径: {save_path}')
    return save_path



def check_and_create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
