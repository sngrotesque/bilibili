from .utils import *
from itertools import count

'''
media_id=1828402584  # 收藏夹ID（必须）
pn=1                 # 页码（必须）
ps=20                # 单页显示数量（必须）
keyword=             # 未知（可选）
order=mtime          # 排序（可选）
type=0               # 类型（可选）
tid=0                # 未知（可选）
platform=web         # 平台（可选）
jsonp=jsonp          # json（可选）
'''

class favlist:
    def __init__(self, fav_id :int, cookie :str = None):
        self.FAV_ID = fav_id
        self.HEADERS = {'user-agent': UserAgent, 'referer': Referer}
        if cookie:
            self.HEADERS['cookie'] = cookie
        self.RESULT_videoInfo = {}

    def getAvID(self):
        serialNumber = 1
        for page in count(start = 0):
            result = RequestGet(self,
                f'https://api.bilibili.com/x/v3/fav/resource/list?media_id={self.FAV_ID}&pn={page}&ps=20'
            ).json()
            if not result['data']['medias']:
                break
            
            for index in range(len(result['data']['medias'])):
                _title = result['data']['medias'][index]['title']
                _avid = result['data']['medias'][index]['link'][17:]
                self.RESULT_videoInfo[f'{serialNumber:0>4}'] = {
                    'title': _title, 'avid': _avid,
                    'link': f"https://www.bilibili.com/video/av{_avid}"
                }
                
                serialNumber += 1







