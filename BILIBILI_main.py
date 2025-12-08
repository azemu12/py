import json
import os
import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger
from data_util import download_video_bilibili

# 往下滑动页面
def scroll_page_end(browser) -> None:
    height = 0
    while height < browser.execute_script("return document.body.clientHeight"):
        height += 400
        browser.execute_script("window.scrollBy(0, 400)")
        time.sleep(2)

def get_all_video_list_by_user_id(driver: uc.Chrome, user_id: str, max_num: int,download_work_max_retry: int):
    """
    获取用户所有视频列表
    :param driver: Chrome 驱动
    :param user_id: 用户ID
    :param max_num: 最大视频数
    :param download_work_max_retry: 下载重试次数
    :return:
    """
    url = f"https://space.bilibili.com/{user_id}/upload/video"
    # 访问目标网页
    driver.get(url)
    # 拿到最大的页数列表
    page_total = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='vui_pagenation--btns']/button[last()-1][@class[contains(., 'vui_pagenation--btn-num')]]"))
    ).text
    page_total = int(page_total)
    logger.info(f"{user_id}总页数{page_total}")
    video_list = []
    for page in range(1, page_total):
        jump_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='number']"))
        )
        jump_input.clear()
        jump_input.send_keys(str(page) + "\n")
        time.sleep(2)
        scroll_page_end(driver)
        # 2 上传csv,勾选第一行为标题行
        vid_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@class="bili-cover-card"]'))
        )
        vid_list = [vid.get_attribute("href").split("/?")[0] for vid in vid_list]
        video_list.extend(vid_list)
        if max_num > 0 and len(video_list) > max_num:
            video_list = video_list[:max_num]
            logger.info(f"{user_id}达到最大视频数{max_num},第{page}页，共{len(video_list)}个视频")
            break
    logger.info(f"{user_id}共{len(video_list)}个视频,{video_list}")
    download_video_bilibili(video_list, download_work_max_retry, f"video_list_{user_id}")
        
    

def main(user_id: str, max_num: int,download_work_max_retry: int):

    # 创建 Chrome 选项并配置下载
    options = uc.ChromeOptions()
    # options.add_argument("--headless=new")     # 无头模式（Chrome 109+ 推荐 new）
    # 启动 Chrome 浏览器
    driver = uc.Chrome(options=options)
    get_all_video_list_by_user_id(driver, user_id, max_num,download_work_max_retry)
    driver.quit()

if __name__ == '__main__':
    download_work_max_retry = 5
    user_id = "480451226"
    max_num = 80
    main(user_id, max_num,download_work_max_retry)
