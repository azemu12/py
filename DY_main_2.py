# coding=utf-8
import json
import os
from loguru import logger
from douyin_api import DouyinAPI
from builder.common_util import init
from data_util_2 import download_work
import sys



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
                download_work(work_info,download_work_max_retry,"all")
            except Exception as e:
                logger.error(f'作品 {work_id} 解析失败: {repr(e)}')
                continue
    def get_user_link_by_user_id(self, auth, user_id: str, get_user_link_max_retry: int) -> dict:
        """
        获取用户信息.
        :param auth: DouyinAuth object.
        :param user_id: 用户id.
        :return: 用户信息.
        """
        return self.douyin_apis.get_user_link_by_user_id(auth, user_id, get_user_link_max_retry)

if __name__ == '__main__':
    # ===== 配置 =====
    date_time = "20260105"
    json_file = f"json/{date_time}_user_id_list.json"  # 你生成的用户列表文件
    progress_file = "progress_0105.json"                # 保存已完成用户
    failed_user_file = "fail_0105.json"               # 失败用户记录
    save_dir = r"/sdc1/mada_16t/download_0119_DY"
    os.makedirs(save_dir, exist_ok=True)     
    get_user_work_info_max_retry = 10
    download_work_max_retry = 10
    get_user_link_max_retry = 10
    work_total_num = 80  # 每个用户要爬取的作品数量

    # 初始化
    auth = init()
    # 初始化对象
    data_spider = Data_Spider()
    # ===== 读取用户列表 =====
    with open(json_file, "r", encoding="utf-8") as f:
        user_data_list = json.load(f)

    # ===== 载入 finished.json =====
    if os.path.exists(progress_file):
        with open(progress_file, "r", encoding="utf-8") as f:
            finished_users = set(json.load(f).get("finished", []))
    else:
        finished_users = set()

    # ===== 载入 failed_users.json =====
    if os.path.exists(failed_user_file):
        with open(failed_user_file, "r", encoding="utf-8") as f:
            failed_users = json.load(f).get("failed", [])
    else:
        failed_users = []

    # ===== 开始处理用户 =====
    for entry in user_data_list:
        user_id = entry["user_id"]
        if user_id in finished_users:
            print(f"跳过已完成用户：{user_id}")
            continue

        try:
            user_url = data_spider.get_user_link_by_user_id(auth, user_id, get_user_link_max_retry)
            
            if not user_url:
                logger.error(f"获取用户 {user_id} 链接失败")

                # 写入 failed_users
                failed_users.append(user_id)
                with open(failed_user_file, "w", encoding="utf-8") as f:
                    json.dump({"failed": failed_users}, f, ensure_ascii=False, indent=2)
                continue

            # 2. 爬取作品
            data_spider.spider_user_all_work(auth, work_total_num, user_url, save_dir,
                                             get_user_work_info_max_retry, download_work_max_retry)

            # 3. 成功后写入 finished_users
            finished_users.add(user_id)
            with open(progress_file, "w", encoding="utf-8") as f:
                json.dump({"finished": list(finished_users)}, f, ensure_ascii=False, indent=2)

        except Exception as e:
            logger.error(f"用户 {user_id} 爬取出错: {repr(e)}")
            # 出错也写入失败文件
            failed_users.append(user_id)
            with open(failed_user_file, "w", encoding="utf-8") as f:
                json.dump({"failed": failed_users}, f, ensure_ascii=False, indent=2)
            continue

    print("执行完毕！")