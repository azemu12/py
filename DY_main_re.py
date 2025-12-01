# coding=utf-8
import json
import os
from loguru import logger
from douyin_api import DouyinAPI
from builder.common_util import init
from data_util import download_work
import sys


class Data_Spider():
    def __init__(self):
        self.douyin_apis = DouyinAPI()

    def spider_user_all_work(self, auth, work_total_num: int, user_url: str, save_dir: str,
                             get_user_work_info_max_retry, download_work_max_retry,
                             downloaded_cache, download_cache_file):

        # 1. 拉取用户所有作品信息
        work_list = self.douyin_apis.get_user_all_work_info(
            auth, user_url, work_total_num, get_user_work_info_max_retry
        )
        if work_list is None:
            logger.error(f'获取用户 {user_url} 全部作品信息失败')
            return

        logger.info(f'用户 {user_url} 获取到作品数量: {len(work_list)}')

        # 2. 过滤掉已经下载的，只收集未下载的视频
        need_download_list = []
        for work_info in work_list:
            work_id = work_info["aweme_id"]

            # 不是视频
            if work_info["aweme_type"] != 0:
                continue

            # 已下载
            if work_id in downloaded_cache:
                logger.info(f"视频 {work_id} 已下载过，跳过")
                continue

            need_download_list.append(work_info)

            # 已达到需要数量
            if len(need_download_list) >= work_total_num:
                break

        logger.info(f"实际需要下载的视频数量: {len(need_download_list)}")

        # 3. 下载视频
        for work_info in need_download_list:
            work_id = work_info["aweme_id"]
            user_id = user_url.split("/")[-1].split("?")[0]

            try:
                work_info["save_path"] = os.path.join(save_dir, user_id, work_id)
                work_info["video_addr"] = work_info["video"]["play_addr"]["url_list"][0]

                download_work(work_info, download_work_max_retry, "all")

                # === 写入到 download_cache.json ===
                downloaded_cache.add(work_id)
                with open(download_cache_file, "w", encoding="utf-8") as f:
                    json.dump({"downloaded": list(downloaded_cache)}, f, ensure_ascii=False, indent=2)

                logger.info(f"视频 {work_id} 下载成功，已加入缓存")

            except Exception as e:
                logger.error(f"作品 {work_id} 下载失败: {repr(e)}")
                continue

    # ---------------------------------------------
    # 获取真实用户主页链接
    # ---------------------------------------------
    def get_user_link_by_user_id(self, auth, user_id: str, get_user_link_max_retry: int) -> dict:
        return self.douyin_apis.get_user_link_by_user_id(auth, user_id, get_user_link_max_retry)


# ============================================================
#                      主运行入口
# ============================================================
if __name__ == '__main__':
    date_time = "20251110"
    json_file = f"json/{date_time}_user_id_list.json"  # 输入用户列表
    progress_file = "progress.json"                     # 已完成用户
    failed_user_file = "fail.json"                      # 失败用户
    download_cache_file = r"/home/gct/DY/json/download_cache.json"         # 已下载视频缓存

    save_dir = r"/sdc1/mada_16t/download_1129"
    os.makedirs(save_dir, exist_ok=True)

    get_user_work_info_max_retry = 10
    download_work_max_retry = 10
    get_user_link_max_retry = 10
    work_total_num = 60     # 每个用户要下载的视频数量

    auth = init()
    data_spider = Data_Spider()

    # 读取用户列表
    with open(json_file, "r", encoding="utf-8") as f:
        user_data_list = json.load(f)

    # ========== 读取 finished.json ==========
    if os.path.exists(progress_file):
        with open(progress_file, "r", encoding="utf-8") as f:
            finished_users = set(json.load(f).get("finished", []))
    else:
        finished_users = set()

    # ========== 读取 failed.json ==========
    if os.path.exists(failed_user_file):
        with open(failed_user_file, "r", encoding="utf-8") as f:
            failed_users = json.load(f).get("failed", [])
    else:
        failed_users = []

    # ========== 读取 download_cache.json ==========
    if os.path.exists(download_cache_file):
        with open(download_cache_file, "r", encoding="utf-8") as f:
            downloaded_cache = set(json.load(f).get("downloaded", []))
    else:
        downloaded_cache = set()

    # ========== 遍历用户并开始下载 ==========
    for entry in user_data_list:
        user_id = entry["user_id"]

        if user_id in finished_users:
            print(f"跳过已完成用户：{user_id}")
            continue

        try:
            # 获取用户主页链接
            user_url = data_spider.get_user_link_by_user_id(auth, user_id, get_user_link_max_retry)

            if not user_url:
                logger.error(f"获取用户 {user_id} 链接失败")

                failed_users.append(user_id)
                with open(failed_user_file, "w", encoding="utf-8") as f:
                    json.dump({"failed": failed_users}, f, ensure_ascii=False, indent=2)
                continue

            # 下载未下载的视频
            data_spider.spider_user_all_work(
                auth,
                work_total_num,
                user_url,
                save_dir,
                get_user_work_info_max_retry,
                download_work_max_retry,
                downloaded_cache,
                download_cache_file
            )

            # 标记完成
            finished_users.add(user_id)
            with open(progress_file, "w", encoding="utf-8") as f:
                json.dump({"finished": list(finished_users)}, f, ensure_ascii=False, indent=2)

        except Exception as e:
            logger.error(f"用户 {user_id} 爬取出错: {repr(e)}")
            failed_users.append(user_id)

            with open(failed_user_file, "w", encoding="utf-8") as f:
                json.dump({"failed": failed_users}, f, ensure_ascii=False, indent=2)
            continue

    print("执行完毕！")
