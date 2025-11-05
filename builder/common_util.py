import os
# from loguru import logger
from dotenv import load_dotenv
from auth import DouyinAuth
dy_auth = None
def load_env():
    global dy_auth
    load_dotenv()
    cookies_dy = os.getenv('DY_COOKIES')
    dy_auth = DouyinAuth()
    dy_auth.perepare_auth(cookies_dy, "", "")
    return dy_auth

def init():
    cookies = load_env()
    return cookies
