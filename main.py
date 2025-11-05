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

    def spider_user_all_work(self, auth, work_total_num: int, user_url: str, save_dir: str,get_user_work_info_max_retry,download_work_max_retry):
        """
        爬取一个用户的所有作品
        :param auth: 用户认证信息
        :param work_total_num: 要获取的作品数量
        :param user_url: 用户链接
        :param save_dir: 保存路径
        :param get_user_work_info_max_retry: 获取用户作品信息最大重试次数
        :param download_work_max_retry: 下载作品最大重试次数
        :param proxies: 代理
        :return:
        """
        # 加载作品列表
        work_list = self.douyin_apis.get_user_all_work_info(auth, user_url, work_total_num,get_user_work_info_max_retry)
        if work_list is None:
            logger.error(f'获取用户 {user_url} 全部作品信息失败')
            return

        logger.info(f'用户 {user_url} 作品数量: {len(work_list)}')

        for work_info in work_list:
            work_id = work_info["aweme_id"]
            user_id = user_url.split("/")[-1].split("?")[0]
            # 判断是否为视频
            if work_info['aweme_type'] != 0:
                logger.info(f'作品 {work_id} 不是视频，跳过')
                continue
            try:
                work_info["save_path"] = os.path.join(save_dir, user_id, work_id)
                work_info["video_addr"] = work_info['video']['play_addr']['url_list'][0]
                download_work(work_info,download_work_max_retry)
            except:
                logger.error(f'作品 {work_info["work_id"]} 解析失败')
                continue

if __name__ == '__main__':

    auth = init()

    data_spider = Data_Spider()
    # 2 爬取用户的所有作品信息 用户链接 如下所示 注意此url会过期！
    user_url = 'https://www.douyin.com/user/MS4wLjABAAAAlnpt6_OsvjEpR6yD-vDGGCroDPcHS25WfPjqVgzt7Du0zJ9oCH1SktFJJey_1Fi8?from_tab_name=main'
    work_total_num = 2000
    save_dir = fr"D:\download_1124"
    get_user_work_info_max_retry = 10
    download_work_max_retry = 10
    data_spider.spider_user_all_work(auth,work_total_num, user_url,save_dir,get_user_work_info_max_retry,download_work_max_retry)
