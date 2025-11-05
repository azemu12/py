import json
import random
import time

from loguru import logger
import requests

from builder.header import HeaderBuilder, HeaderType
from builder.params import Params
import random



class DouyinAPI:
    douyin_url = 'https://www.douyin.com'
    douyin_url_user_new = 'https://www-hj.douyin.com'

    @staticmethod
    def get_user_all_work_info(auth, user_url: str, num: int, max_retry: int = 3, **kwargs) -> list:
        """
        获取用户全部作品信息.
        :param auth: DouyinAuth object.
        :param user_url: 用户主页URL.
        :return: 全部作品信息.
        """
        max_cursor = "0"
        work_list = []
        while True:
            res_json = DouyinAPI.get_user_work_info(auth, user_url, max_cursor, max_retry=max_retry)
            if "aweme_list" not in res_json.keys():
                logger.info(f"get_user_all_work_info_获取用户{user_url}全部作品信息失败,已获取到{len(work_list)}条")
                break
            works = res_json["aweme_list"]
            max_cursor = str(res_json["max_cursor"])
            work_list.extend(works)
            if res_json["has_more"] != 1 or (num != 0 and len(work_list) >= num):
                break
        return work_list


    @staticmethod
    def get_user_work_info(auth, user_url: str, max_cursor, max_retry: int = 3) -> dict:
        """
        获取用户作品信息.
        :param auth: DouyinAuth object.
        :param user_url:  用户主页URL.
        :param max_cursor:  上一次请求的max_cursor.
        :return:
        """
        api = f"/aweme/v1/web/aweme/post"
        user_id = user_url.split("/")[-1].split("?")[0]
        headers = HeaderBuilder().build(HeaderType.GET)
        headers.set_referer(user_url)
        params = Params()
        params.add_param("device_platform", 'webapp')
        params.add_param("aid", '6383')
        params.add_param("channel", 'channel_pc_web')
        params.add_param("sec_user_id", user_id)
        params.add_param("max_cursor", max_cursor)
        params.add_param("locate_query", 'false')
        params.add_param("show_live_replay_strategy", '1')
        params.add_param("need_time_list", '1' if max_cursor == '0' else '0')
        params.add_param("time_list_query", '0')
        params.add_param("whale_cut_token", '')
        params.add_param("cut_version", '1')
        params.add_param("count", '18')
        params.add_param("publish_video_strategy_type", '2')
        params.add_param("update_version_code", '170400')
        params.add_param("pc_client_type", '1')
        params.add_param("version_code", '290100')
        params.add_param("version_name", '29.1.0')
        params.add_param("cookie_enabled", 'true')
        params.add_param("screen_width", '1707')
        params.add_param("screen_height", '960')
        params.add_param("browser_language", 'zh-CN')
        params.add_param("browser_platform", 'Win32')
        params.add_param("browser_name", 'Edge')
        params.add_param("browser_version", '125.0.0.0')
        params.add_param("browser_online", 'true')
        params.add_param("engine_name", 'Blink')
        params.add_param("engine_version", '125.0.0.0')
        params.add_param("os_name", 'Windows')
        params.add_param("os_version", '10')
        params.add_param("cpu_core_num", '32')
        params.add_param("device_memory", '8')
        params.add_param("platform", 'PC')
        params.add_param("downlink", '10')
        params.add_param("effective_type", '4g')
        params.add_param("round_trip_time", '100')
        params.with_web_id(auth, user_url)
        params.add_param("verifyFp", auth.cookie['s_v_web_id'])
        params.add_param("fp", auth.cookie['s_v_web_id'])
        params.add_param("msToken",
                         auth.msToken)
        for attempt in range(2):
            try:
                resp = requests.get(f'{DouyinAPI.douyin_url_user_new}{api}', headers=headers.get(), cookies=auth.cookie,
                                    params=params.get(), verify=False)
                resp.raise_for_status()
                resp_json = json.loads(resp.text)
                if resp_json.get("status_code") == 0:
                    logger.info(f"get_user_work_info_获取用户{user_id}第{max_cursor}页成功")
                    return resp_json
                else:
                    logger.info(f"get_user_work_info_获取用户{user_id}第{max_cursor}页失败, 响应体: {resp_json}")
            except Exception as e:
                logger.error(f"get_user_work_info_获取用户{user_id}第{max_cursor}页失败 {e} 响应码非200 重试 {attempt + 1}次")
        return None 

