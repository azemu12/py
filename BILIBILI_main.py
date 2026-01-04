import json
import os
import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger

# 时间转换为秒数


def time_to_seconds(time_str: str) -> int:
    """
    将形如 HH:MM:SS / MM:SS / SS 的字符串转换为秒数
    """
    if not time_str or not isinstance(time_str, str):
        return 0

    parts = time_str.strip().split(":")
    parts = [p for p in parts if p != ""]  # 去掉空组件

    # 只要不是数字，就直接返回 0
    if not all(p.isdigit() for p in parts):
        return 0

    # 根据长度计算
    if len(parts) == 3:      # HH:MM:SS
        h, m, s = map(int, parts)
    elif len(parts) == 2:    # MM:SS
        h = 0
        m, s = map(int, parts)
    elif len(parts) == 1:    # SS
        return int(parts[0])
    else:                    # 其它不合法情况
        return 0

    return h * 3600 + m * 60 + s
# 往下滑动页面


def scroll_page_end(browser) -> None:
    height = 0
    while height < browser.execute_script("return document.body.clientHeight"):
        height += 400
        browser.execute_script("window.scrollBy(0, 400)")
        time.sleep(2)


def get_all_video_list_by_user_id(
        driver: uc.Chrome, user_id: str, max_num: int, video_time_max: int
):
    """
    获取用户所有视频列表
    :param driver: Chrome 驱动
    :param user_id: 用户ID
    :param max_num: 最大视频数 (0 表示不限)
    :param video_time_max: 视频最大时长(秒)
    """
    url = f"https://space.bilibili.com/{user_id}/upload/video"
    logger.info(f"{user_id} 获取视频列表 {url}")
    driver.get(url)

    # 获取总页数
    try:
        page_total = int(WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='vui_pagenation--btns']/button[last()-1][contains(@class,'vui_pagenation--btn-num')]")
            )
        ).text)
        logger.info(f"{user_id} 总页数 {page_total}")
    except Exception:
        logger.warning(f"{user_id} 获取总页数失败，默认 1 页")
        page_total = 1

    video_list: list[str] = []

    # 逐页处理
    for page in range(1, page_total + 1):

        # 页码跳转（第1页不跳避免卡顿）
        if page > 1:
            try:
                jump_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='number']"))
                )
                jump_input.clear()
                jump_input.send_keys(str(page) + "\n")
                time.sleep(1.8)
            except Exception:
                logger.error(f"{user_id} 第 {page} 页跳转失败，结束采集")
                break

        scroll_page_end(driver)

        try:
            vid_cards = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//a[contains(@class,"bili-cover-card")]')
                )
            )
        except Exception:
            logger.warning(f"{user_id} 第 {page} 页无视频，跳过")
            continue

        for card in vid_cards:
            try:
                duration_text = card.find_element(
                    By.XPATH, './/div[@class="bili-cover-card__stats"]//div[3]'
                ).text
                if time_to_seconds(duration_text) > video_time_max:
                    continue

                url = card.get_attribute("href").split("/?")[0]
                video_list.append(url)

                # 达到最大数量退出
                if max_num > 0 and len(video_list) >= max_num:
                    logger.info(f"{user_id} 达到最大视频数 {max_num}，采集结束")
                    return video_list
            except Exception:
                continue

        logger.info(f"{user_id} 第 {page} 页已采集 {len(video_list)} 个视频")

    return video_list



def main(user_id_list: list, max_num: int, video_time_max: int):

    # 创建 Chrome 选项并配置下载
    options = uc.ChromeOptions()
    # options.add_argument("--headless=new")     # 无头模式（Chrome 109+ 推荐 new）
    # 启动 Chrome 浏览器
    driver = uc.Chrome(options=options)
    try:
        with open("video_href.json", "r",encoding="utf-8") as f:
            lines = [json.loads(line) for line in f]   # 读一次
        have_user_id = [item["user_id"] for item in lines]
        max_index = max(int(item["index"]) for item in lines)
    except FileNotFoundError:
        have_user_id = []
        max_index = 0
    with open("video_href.json", "a+",encoding="utf-8") as f:
        index = max_index+1
        for user_id in user_id_list:
            if user_id in have_user_id:
                continue
            video_list = get_all_video_list_by_user_id(driver, user_id, max_num, video_time_max)
            for video_id in video_list:
                f.write(json.dumps({
                    "index": f"{index:05d}",
                    "user_id": user_id,
                    "video_href": video_id
                }, ensure_ascii=False) + "\n")
                index += 1
    driver.quit()
    return "success"


if __name__ == '__main__':
    user_id_list = [

"5012400",
"399655394",
"421386209",
"11721556",
"639992213",
"400211388",
"492606139",
"329342508",
"16167325",
"21563304",
"2009929",
"3546648112270150",
"533996453",
"2378703",
"478371409",
"1031626657",
"1049355617",
"564429853",
"354033527",
"39207642",
"400844186",
"3546954776709189",
"521665433",
"627140423",
"544006385",
"28751000",
"345557409",
"2804493",
"805203",
"81355943",
"146188283",
"99639987",
"26177922",
"2528402",
"116683",
"8915872",
"43724742",
"15434335",
"403611817",
"398011818",
"356546643",
"3690971877345581",
"241293573",
"327798094",
"407039398",
"17614942",
"544007575",
"3461576537409860",
"15107703",
"1340397556",
"527428753",
"442375417",
"21566099",
"3546722240301816",
"349316844",
"1366664945",
"3546964004178736",
"3546574368016518",
"1344227",
"3546649865489128",
"1166443766",
"3537106366367822",
"34967693",
"88197275",
"1524096397",
"36811595",
"42886922"


    ]
    max_num = 80
    video_time_max = 120
    while True:
        ret = main(user_id_list, max_num, video_time_max)
        if ret == "success":
            break
