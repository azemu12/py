import os
import time
import random
import yt_dlp
dirs = r'0908_music_download'

def download_video(dirs, file_name, file_url,cookie_path):
    def _run_download(use_cookies=False):
        ydl_opts_download = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(dirs, file_name),
            # 'proxy': proxy,
            'merge_output_format': 'mp4',
            'quiet': True,
            'verbose': True,
            'retries': 5,
            'continuedl': True,
            'concurrent_fragment_downloads': 10,  # 多分片并行
            'noprogress': False,  # 显示进度
        }

        if use_cookies:
            ydl_opts_download['cookies'] = cookie_path
            print(f"⚠️ 使用 Cookie 文件重试下载: {file_name}")

        with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
            ydl.download([file_url])

    try:
        # 第一次尝试，不使用 cookie
        _run_download(use_cookies=False)
        print(f"{file_name} 下载成功 ✅（无 Cookie）")
        return 1

    except Exception as e1:
        print(f"{file_name} 第一次下载失败 ❌，错误：{e1}")
        time.sleep(random.randint(1, 3))

        try:
            # 第二次尝试，使用 cookie
            _run_download(use_cookies=True)
            print(f"{file_name} 下载成功 ✅（使用 Cookie）")
            return 1

        except Exception as e2:
            print(f"{file_name} 下载失败 ❌（使用 Cookie 后仍失败），错误：{e2}")
            return -1

if __name__ == '__main__':
    video_list = ['https://www.bilibili.com/video/BV17VmcBJEAS/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1U3mwBzECY/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1DMmwBrEP4/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV18R2XBJEvk/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1f729BYEg6/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV19e2WBgEos/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1EZ2JBMEwT/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV16QS4BKEWd/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV11bSnBoEEH/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1dkSjBaEFD/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV15HUrBcE4Y/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV13sUTBFEBY/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1AiUxBvEgS/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1xDypBXEC6/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV15eypBeEAz/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1zByJBPEfP/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1vay3BKE1x/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV19ACuBWEwh/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1HTCgB6EXS/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1e6CTBnEFs/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1rCC7BFETP/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV118CLBFET6/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV134kiBfEra/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1vHkfBhE5h/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1LzkZBcEmR/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1Kuk9BNEjR/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1L2kDBGEEi/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1t7kUBWEgk/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1W111BEE4M/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1Ui2MBXExi/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1iA1xBjEmd/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV16K1CBTE9X/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1Dp1rBmEBJ/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV16C1rBPEmH/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1pJ1kBzEHo/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1tG1YBpEyU/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1Xm1cBuEiX/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV13U1cBBESZ/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1kCyZBLEYV/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1DKyfBbEYA/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1VTyQB1EYK/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV15N15BLERv/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1Ns15BaESg/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1VF1gBAEWY/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1kc1uBkErt/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1MA1KByEtk/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1e81PBEEbb/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1CGyaB6EBY/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1NuyaBkEwM/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV186yaBHEns/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1U6y8BkEcG/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1Vty8BQEZe/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1YTybBjEeH/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1NPy8BMExB/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1iZyxByEui/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1SMymBtEYP/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV13VykBSEo1/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1ruyzBREwP/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1zjsmz5EgD/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1tjs2zsETv/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV19ys2zKEih/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1gwskzJEJr/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1DwxNz2EBN/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1HPxKzNEP7/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1xDxAzKE1x/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1mfsZzsEEu/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1Wksoz7Ead/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1kcsRzqEa4/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1M3sdzSEMz/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1sasXzBEZj/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1ugsWzcESE/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1x7sWzxEkS/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1gNsHzdEVB/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1RisHzeEBa/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1HWsHzCE4V/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV17bsJzaEEk/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV15xsBzjEiC/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV1GYWRzXEs7/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV17PWdzhETU/?spm_id_from=333.1387.upload.video_card.click', 'https://www.bilibili.com/video/BV14pW9z6EeS/?spm_id_from=333.1387.upload.video_card.click']
    video_list = [v.split("/?")[0] for v in video_list]
    for video_url in video_list:
        file_name = video_url.split("/")[-1]
        download_video(dirs, file_name, video_url, "1.txt")
