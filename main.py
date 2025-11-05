# coding=utf-8
import json
import os
from loguru import logger
from douyin_api import DouyinAPI
from builder.common_util import init


class Data_Spider():
    def __init__(self):
        self.douyin_apis = DouyinAPI()

    def spider_user_all_work(self, auth, num: int, user_url: str,proxies=None):
        """
        爬取一个用户的所有作品
        :param auth: 用户认证信息
        :param num: 要获取的作品数量
        :param user_url: 用户链接
        :param base_path: 保存路径
        :param proxies: 代理
        :return:
        """
        # 加载作品列表
        work_list = self.douyin_apis.get_user_all_work_info(auth, user_url, num=num,max_retry=10)
        if work_list is None:
            logger.error(f'获取用户 {user_url} 全部作品信息失败')
            return

        logger.info(f'用户 {user_url} 作品数量: {len(work_list)}')

        for work_info in work_list:
            with open("test.json", "w", encoding="utf-8") as f:
                json.dump(work_info, f, ensure_ascii=False, indent=4)
            # work_info = handle_work_info(work_info)
            # logger.info(f'爬取作品信息 {work_info["work_url"]}')
            # work_info["save_path"] = fr"D:\download\{user_url.split('/')[-1].split('?')[0]}"
            # download_work(work_info, base_path['media'], save_choice)

if __name__ == '__main__':

    auth = init()

    data_spider = Data_Spider()
    # 2 爬取用户的所有作品信息 用户链接 如下所示 注意此url会过期！
    user_url = 'https://www.douyin.com/user/MS4wLjABAAAAaCcBHb3Rhc4zxF8YkBOfHfLh6k-IWEK2l3Ne9xOXPnQ'
    num = 2000
    data_spider.spider_user_all_work(auth,num, user_url)
