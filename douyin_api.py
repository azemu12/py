import json
import random
import time
import urllib
import uuid
from loguru import logger
import requests

from builder.header import HeaderBuilder, HeaderType
from builder.params import Params
import random


class DouyinAPI:
    douyin_url = 'https://www.douyin.com'
    hj_douyin_url = 'https://www-hj.douyin.com/'
    @staticmethod
    def get_user_all_work_info(auth, user_url: str, work_total_num: int, get_user_work_info_max_retry: int) -> list:
        """
        获取用户全部作品信息.
        :param auth: DouyinAuth object.
        :param user_url: 用户主页URL.
        :return: 全部作品信息.
        """
        max_cursor = "0"
        work_list = []
        while True:
            res_json = DouyinAPI.get_user_work_info(auth, user_url, max_cursor, get_user_work_info_max_retry)
            if "aweme_list" not in res_json.keys():
                logger.info(f"get_user_all_work_info_获取用户{user_url}全部作品信息失败,已获取到{len(work_list)}条")
                break
            works = res_json["aweme_list"]
            max_cursor = str(res_json["max_cursor"])
            work_list.extend(works)
            if res_json["has_more"] != 1 or (work_total_num != 0 and len(work_list) >= work_total_num):
                break
        return work_list

    @staticmethod
    def get_user_work_info(auth, user_url: str, max_cursor, get_user_work_info_max_retry: int) -> dict:
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
        params.add_param("msToken",auth.msToken)
        for attempt in range(get_user_work_info_max_retry):
            try:
                resp = requests.get(f'{DouyinAPI.douyin_url}{api}', headers=headers.get(), cookies=auth.cookie,
                                    params=params.get(), verify=False)
                resp.raise_for_status()
                resp_json = json.loads(resp.text)
                if resp_json.get("status_code") == 0:
                    logger.info(
                        f"get_user_work_info_获取用户{user_id}第{max_cursor}页成功")
                    return resp_json
                else:
                    logger.info(
                        f"get_user_work_info_获取用户{user_id}第{max_cursor}页失败, 响应体: {resp_json}")
            except Exception as e:
                logger.error(
                    f"get_user_work_info_获取用户{user_id}第{max_cursor}页失败 {e} 响应码非200 重试 {attempt + 1}次")
        return None
    @staticmethod
    def get_user_link_by_user_id(auth, user_id: str, get_user_link_max_retry: int) -> str:
        """
        获取用户链接.
        :param auth: DouyinAuth object.
        :param user_id: 用户id.
        :return: 用户链接.
        """
        user_list = DouyinAPI.get_all_user_link_by_user_id(auth, user_id, get_user_link_max_retry)
        if len(user_list) == 0:
            logger.info(f"get_user_link_by_user_id_获取用户{user_id}失败, 未找到相关数据")
            return ""
        else:
            for user_item in user_list:
                if user_item["user_info"]["unique_id"] == user_id:
                    user_link = f"https://www.douyin.com/user/{user_item["user_info"]["sec_uid"]}"
                    logger.info(f"get_user_link_by_user_id_获取用户{user_id}成功, 用户链接: {user_link}")
                    return user_link
            logger.info(f"get_user_link_by_user_id_获取用户{user_id}失败, 未找到相关数据")

    @staticmethod
    def get_all_user_link_by_user_id(auth, user_id: str, get_user_link_max_retry: int) -> dict:
        """
        获取用户信息.
        :param auth: DouyinAuth object.
        :param user_url: 用户id.
        :return: 用户信息.
        """
        api = "/aweme/v1/web/discover/search"
        headers = HeaderBuilder().build(HeaderType.GET)
        refer = f'https://www.douyin.com/search/{urllib.parse.quote(user_id)}?aid={uuid.uuid4()}&type=general'
        headers.set_referer(refer)
        params = Params()
        params.add_param("device_platform", 'webapp')
        params.add_param("aid", '6383')
        params.add_param("channel", 'channel_pc_web')
        params.add_param("search_channel", 'aweme_user_web')
        params.add_param("keyword", user_id)
        params.add_param("search_source", 'switch_tab')
        params.add_param("query_correct_type", '1')
        params.add_param("is_filter_search", '1')
        # params.add_param("from_group_id", '7378456704385600820')
        params.add_param("offset", '0')
        params.add_param("count", '25')
        params.add_param("need_filter_settings", '1')
        params.add_param("list_type", 'single')
        params.add_param("update_version_code", '170400')
        params.add_param("pc_client_type", '1')
        params.add_param("version_code", '170400')
        params.add_param("version_name", '17.4.0')
        params.add_param("cookie_enabled", 'true')
        params.add_param("screen_width", '1707')
        params.add_param("screen_height", '960')
        params.add_param("browser_language", 'zh-CN')
        params.add_param("browser_platform", 'Win32')
        params.add_param("browser_name", 'Edge')
        params.add_param("browser_version", '142.0.0.0')
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
        params.add_param("round_trip_time", '150')
        params.with_web_id(auth, refer)
        params.add_param("msToken", auth.msToken)
        params.with_a_bogus()
        for attempt in range(1):
            try:
                resp = requests.get(f'{DouyinAPI.douyin_url}{api}', headers=headers.get(), cookies=auth.cookie,
                                    params=params.get(), verify=False)
                resp.raise_for_status()
                resp_json = json.loads(resp.text)
                if resp_json.get("status_code") == 0:
                    logger.info(f"get_user_link_by_user_id_获取用户{user_id}成功")
                    return resp_json["user_list"]
                else:
                    logger.info(f"get_user_link_by_user_id_获取用户{user_id}失败, 响应体: {resp_json}")
            except Exception as e:
                logger.error(f"get_user_link_by_user_id_获取用户{user_id}失败 {e} 响应码非200 重试 {attempt + 1}次")
        return None 
    @staticmethod
    def get_work_id_by_share_href(share_href: str, get_work_id_by_share_href_max_retry: int) -> str:
        """
        根据分享链接获取作品id.
        :param share_href: 分享链接.
        :return: 作品id.
        """
        for i in range(get_work_id_by_share_href_max_retry):
            try:
                response = requests.get(share_href, allow_redirects=True)
                response_url = response.url
                if "/?" in response_url:
                    work_id = response_url.split("/?")[0].split("/")[-1]
                else:
                    work_id = response_url.split("/")[-1].split("?")[0]
                logger.info(f"get_work_id_by_share_href_获取作品id成功 work_id: {work_id}")
                return work_id
            except Exception as e:
                logger.error(f"get_work_id_by_share_href_获取作品id失败 {e} 重试 {i + 1}次")
        return ""   

    @staticmethod
    def get_video_arrd_by_work_id(auth, work_id: str, get_video_arrd_by_work_id_max_retry: int) -> dict:
        """
        根据work_id获取视频下载链接.
        :param auth: DouyinAuth object.
        :param work_id: 作品id.
        :return: 视频下载链接.
        """
        api = "/aweme/v1/web/aweme/detail"
        headers = HeaderBuilder().build(HeaderType.GET)
        refer = f'https://www.douyin.com/'
        headers.set_referer(refer)
        params = Params()
        params.add_param("device_platform", "webapp")
        params.add_param("aid", "6383")
        params.add_param("channel", "channel_pc_web")
        params.add_param("aweme_id", work_id)
        params.add_param("update_version_code", "170400")
        params.add_param("pc_client_type", "1")
        params.add_param("pc_libra_divert", "Windows")
        params.add_param("support_h265", "1")
        params.add_param("support_dash", "1")
        params.add_param("cpu_core_num", "16")
        params.add_param("version_code", "190500")
        params.add_param("version_name", "19.5.0")
        params.add_param("cookie_enabled", "true")
        params.add_param("screen_width", "1920")
        params.add_param("screen_height", "1080")
        params.add_param("browser_language", "zh-CN")
        params.add_param("browser_platform", "Win32")
        params.add_param("browser_name", "Edge")
        params.add_param("browser_version", "142.0.0.0")
        params.add_param("browser_online", "true")
        params.add_param("engine_name", "Blink")
        params.add_param("engine_version", "142.0.0.0")
        params.add_param("os_name", "Windows")
        params.add_param("os_version", "10")
        params.add_param("device_memory", "8")
        params.add_param("platform", "PC")
        params.add_param("downlink", "10")
        params.add_param("effective_type", "4g")
        params.add_param("round_trip_time", "50")
        params.with_web_id(auth, refer)
        params.add_param("verifyFp", auth.cookie['s_v_web_id'])
        params.add_param("fp", auth.cookie['s_v_web_id'])
        params.add_param("msToken",auth.msToken)
        params.with_a_bogus()
        for attempt in range(get_video_arrd_by_work_id_max_retry):
            try:
                resp = requests.get(f'{DouyinAPI.hj_douyin_url}{api}', headers=headers.get(), cookies=auth.cookie,
                                    params=params.get(), verify=False)
                resp.raise_for_status()
                resp_json = json.loads(resp.text)
                if resp_json.get("status_code") == 0:
                    logger.info(f"get_video_arrd_by_work_id_{work_id}获取下载链接成功")
                    return resp_json["aweme_detail"]["video"]["play_addr"]["url_list"][0]
                else:
                    logger.info(f"get_video_arrd_by_work_id_{work_id}获取下载链接失败, 响应体: {resp_json}")
            except Exception as e:
                logger.error(f"get_video_arrd_by_work_id_{work_id}获取下载链接失败 {e} 响应码非200 重试 {attempt + 1}次")
        return None 