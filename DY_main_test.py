# coding=utf-8
import os
import json
import requests
from loguru import logger

from douyin_api import DouyinAPI
from builder.common_util import init


# ===================== 下载函数 =====================
def download_video(url, save_path, filename):
    os.makedirs(save_path, exist_ok=True)
    file_path = os.path.join(save_path, filename)

    if os.path.exists(file_path):
        logger.info(f"已存在，跳过: {file_path}")
        return

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Referer": "https://www.douyin.com/",
        "Accept": "*/*",
    }

    with requests.get(
        url,
        headers=headers,
        stream=True,
        allow_redirects=True,
        timeout=30,
    ) as r:
        r.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    logger.success(f"下载完成: {file_path}")


# ===================== 爬虫类 =====================
class DataSpider:
    def __init__(self):
        self.api = DouyinAPI()

    def spider_user_all_work(self, auth, user_url, save_dir, limit, retry):
        work_list = self.api.get_user_all_work_info(auth, user_url, limit, retry)
        if not work_list:
            logger.warning(f"{user_url} 没有可下载作品")
            return False

        user_id = user_url.split("/")[-1].split("?")[0]
        logger.info(f"用户 {user_id} 作品数: {len(work_list)}")

        for work in work_list:
            # ⚠️ 不再限制 aweme_type
            if "video" not in work:
                continue

            work_id = work["aweme_id"]
            logger.info(f"处理作品 {work_id}")

            try:
                download_url = work["video"]["play_addr"]["url_list"][0]
                save_path = os.path.join(save_dir, user_id)
                download_video(download_url, save_path, f"{work_id}.mp4")
            except Exception as e:
                logger.error(f"{work_id} 下载失败: {e}")

        return True


# ===================== 主入口 =====================
if __name__ == "__main__":
    # -------- 配置 --------
    date_time = "202512167"
    user_json = f"json/{date_time}_user_id_list.json"
    progress_file = "progress_1222.json"
    failed_file = "failed_1222.json"
    save_dir = "/sdc1/mada_16t/download_1222_DY"

    limit = 80
    retry = 10

    os.makedirs(save_dir, exist_ok=True)

    # -------- 初始化 --------
    auth = init()
    spider = DataSpider()

    # -------- 读取用户列表 --------
    with open(user_json, "r", encoding="utf-8") as f:
        user_list = json.load(f)

    # -------- 读取进度 --------
    finished = set()
    if os.path.exists(progress_file):
        finished = set(json.load(open(progress_file))["finished"])

    failed = []
    if os.path.exists(failed_file):
        failed = json.load(open(failed_file))["failed"]

    # -------- 主循环 --------
    for item in user_list:
        user_id = item["user_id"]

        if user_id in finished:
            logger.info(f"跳过已完成用户 {user_id}")
            continue

        try:
            user_url = spider.api.get_user_link_by_user_id(auth, user_id, retry)
            if not user_url:
                raise Exception("获取用户链接失败")

            ok = spider.spider_user_all_work(
                auth=auth,
                user_url=user_url,
                save_dir=save_dir,
                limit=limit,
                retry=retry,
            )

            if ok:
                finished.add(user_id)
                json.dump(
                    {"finished": list(finished)},
                    open(progress_file, "w"),
                    ensure_ascii=False,
                    indent=2,
                )

        except Exception as e:
            logger.error(f"用户 {user_id} 失败: {e}")
            failed.append(user_id)
            json.dump(
                {"failed": failed},
                open(failed_file, "w"),
                ensure_ascii=False,
                indent=2,
            )

    print("执行完毕")
