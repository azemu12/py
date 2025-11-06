import requests

url = "https://v.douyin.com/zmvtPB7lFis/"  # 原始短链接
response = requests.get(url, allow_redirects=True)
response_url = response.url
if "/?" in response_url:
    work_id = response_url.split("/?")[0].split("/")[-1]
else:
    work_id = response_url.split("/")[-1].split("?")[0]
print(work_id)
print(response_url)
