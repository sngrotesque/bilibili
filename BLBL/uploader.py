from .utils import *

class up_info:
    def __init__(self, mid :str):
        self.DEFINED_mid = mid
        self.DEFINED_HTTP_Headers = { # 设定HTTP请求头
            'referer': f'https://space.bilibili.com/{self.DEFINED_mid}',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
        }

    @property
    def GetUpName(self):
        url = f'https://api.bilibili.com/x/space/acc/info?mid={self.DEFINED_mid}&jsonp=jsonp'
        res = rget(url, headers = self.DEFINED_HTTP_Headers).json()
        return res['data']['name']

    @property
    def GetUpAvatar(self):
        url = f'https://api.bilibili.com/x/space/acc/info?mid={self.DEFINED_mid}&jsonp=jsonp'
        res = rget(url, headers = self.DEFINED_HTTP_Headers).json()
        return res['data']['face']

    @property
    def GetUpDocument(self):
        url = f'https://api.bilibili.com/x/space/acc/info?mid={self.DEFINED_mid}&jsonp=jsonp'
        res = rget(url, headers = self.DEFINED_HTTP_Headers).json()
        return res['data']['sign']
