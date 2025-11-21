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


    def spider_video_arrd_by_share_href(self, auth, share_href: str, save_dir: str, date_time: str, save_id: str, get_video_arrd_by_work_id_max_retry: int) -> dict:
        """
        根据work_id获取视频下载链接.
        :param auth: DouyinAuth object.
        :param work_id: 作品id.
        :return: 视频下载链接.
        """
        work_id = self.douyin_apis.get_work_id_by_share_href(share_href, get_video_arrd_by_work_id_max_retry)
        if work_id == "":
            logger.error(f"get_work_id_by_share_href_获取作品id失败 share_href: {save_id}")
            return
        video_arrd = self.douyin_apis.get_video_arrd_by_work_id(auth, work_id, get_video_arrd_by_work_id_max_retry)
        if video_arrd == None:
            logger.error(f"get_video_arrd_by_work_id_获取视频下载链接失败 share_href: {save_id}")
            return
        work_info = {}
        work_info["video_addr"] = video_arrd
        work_info["save_path"] = os.path.join(save_dir, date_time, save_id)
        work_info["aweme_id"] = work_id
        download_work(work_info,download_work_max_retry,download_type="one")


if __name__ == '__main__':
    # ===== 配置 =====
    date_time = "20251105"
    json_file = f"json/{date_time}_video_href.json"  # 你生成的用户列表文件
    save_dir = fr"D:\download_1105"
    os.makedirs(save_dir, exist_ok=True)
    # ===== 重试次数 =====
    # 获取用户全部作品信息最大重试次数
    get_user_work_info_max_retry = 10
    # 下载作品最大重试次数
    download_work_max_retry = 10
    # 获取用户链接最大重试次数
    get_user_link_max_retry = 10
    # 根据work_id获取视频下载链接最大重试次数   
    get_video_arrd_by_work_id_max_retry = 10
    work_total_num = 0

    # 初始化
    auth = init()
    # 初始化对象
    data_spider = Data_Spider()
    with open(json_file, 'r', encoding='utf-8') as f:
        user_id_list = json.load(f)
    already_downloaded = set([os.path.splitext(file)[0] for file in os.listdir(os.path.join(save_dir, date_time))])
    for user_id in user_id_list:
        share_href = user_id["video_href"]
        save_id = user_id["id"]
        if save_id in already_downloaded:
            print(f"跳过已完成用户：{save_id}")
            continue
        data_spider.spider_video_arrd_by_share_href(auth, share_href, save_dir,date_time,save_id,get_video_arrd_by_work_id_max_retry)
