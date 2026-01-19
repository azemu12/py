import requests

cookies = {
    'visitor-uuid': '004944db-3b08-4a65-80c6-da83ae84a37c',
    '__stripe_mid': '67d4140f-df3b-46df-bc1f-2eb47cb596848b2417',
    '__cf_bm': 's3FzkwdtFRELglvOLq4eO7Ogu8jA9MDEAJYBPqElJ.M-1767601460-1.0.1.1-6y6cxiK1403WXfKgKTKv5sI13WCfLsIYHSQDI6yCR5cN5IPo4nFoir4oSd6I7Z9PI7vaG1aUQ4uPBgVaM9uO9sjeSxFVsZ.Y0LoQtU7zpBcjN_WN4gww7zgi4Wkd4wGy',
    'PRIVATE-CSRF-TOKEN': '38YEPiOQjjA3c7prgM9uW0DEOvgFnAn2gFDtUWxa%2B8A%3D',
    '__stripe_sid': '879155d9-be97-4c11-aef4-168db1d47629f30416',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.artstation.com/?sort_by=community&dimension=all',
    'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
    # 'cookie': 'visitor-uuid=004944db-3b08-4a65-80c6-da83ae84a37c; __stripe_mid=67d4140f-df3b-46df-bc1f-2eb47cb596848b2417; __cf_bm=s3FzkwdtFRELglvOLq4eO7Ogu8jA9MDEAJYBPqElJ.M-1767601460-1.0.1.1-6y6cxiK1403WXfKgKTKv5sI13WCfLsIYHSQDI6yCR5cN5IPo4nFoir4oSd6I7Z9PI7vaG1aUQ4uPBgVaM9uO9sjeSxFVsZ.Y0LoQtU7zpBcjN_WN4gww7zgi4Wkd4wGy; PRIVATE-CSRF-TOKEN=38YEPiOQjjA3c7prgM9uW0DEOvgFnAn2gFDtUWxa%2B8A%3D; __stripe_sid=879155d9-be97-4c11-aef4-168db1d47629f30416',
}

params = {
    'page': '4',
    'per_page': '30',
}
proxies = {
    "http": "http://192.168.10.48:7890",
    "https":"http://192.168.10.48:7890"
}
response = requests.get(
    'https://www.artstation.com/api/v2/neighborhoods/projects/community.json',
    params=params,
    cookies=cookies,
    headers=headers,
    proxies=proxies,
    timeout=5
)
print(response.json())
print(response.status_code)