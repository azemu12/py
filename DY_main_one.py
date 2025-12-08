# coding=utf-8
import json
import os
from loguru import logger
from douyin_api import DouyinAPI
from builder.common_util import init
from data_util import download_work


class Data_Spider():
    def __init__(self):
        self.douyin_apis = DouyinAPI()

    def spider_video_arrd_by_share_href(self, auth, share_href: str, save_dir: str,
                                        date_time: str, save_id: str,
                                        get_video_arrd_by_work_id_max_retry: int) -> dict:
        """
        根据 share_href 获取视频下载链接.
        """
        work_id = self.douyin_apis.get_work_id_by_share_href(
            share_href, get_video_arrd_by_work_id_max_retry
        )
        if work_id == "":
            logger.error(f"获取作品ID失败 share_href: {save_id}")
            return

        video_arrd = self.douyin_apis.get_video_arrd_by_work_id(
            auth, work_id, get_video_arrd_by_work_id_max_retry
        )
        if video_arrd is None:
            logger.error(f"获取视频下载链接失败 share_href: {save_id}")
            return

        work_info = {
            "video_addr": video_arrd,
            "save_path": os.path.join(save_dir, f"{date_time}_{save_id}"),
            "aweme_id": work_id,
        }

        download_work(work_info, download_work_max_retry, download_type="one")


if __name__ == '__main__':
    # ===== 配置 =====
    date_time = "20251201"
    json_file = f"json/{date_time}_video_href.json"
    save_dir = r"/sdc1/mada_16t/download_1204"

    # ===== 只创建这个目录 =====
    os.makedirs(save_dir, exist_ok=True)

    # ===== 重试次数 =====
    get_user_work_info_max_retry = 10
    download_work_max_retry = 10
    get_user_link_max_retry = 10
    get_video_arrd_by_work_id_max_retry = 10

    # 初始化
    auth = init()
    data_spider = Data_Spider()

    # 读取 JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        user_id_list = json.load(f)

    # 读取已下载过的 id（不需要子目录）
    already_downloaded = set([
        os.path.splitext(file)[0]
        for file in os.listdir(save_dir)
    ])

    # ===== 主循环 =====
    for user in user_id_list:
        share_href = user["video_href"]
        save_id = user["id"]

        if save_id in already_downloaded:
            print(f"跳过已完成：{save_id}")
            continue

        data_spider.spider_video_arrd_by_share_href(
            auth,
            share_href,
            save_dir,
            date_time,
            save_id,
            get_video_arrd_by_work_id_max_retry
        )
