from .utils import *

UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'

class up_info:
    '''通过UID获取UP主的各种信息，不过小心批量爬取会被封IP'''
    def __init__(self, mid :str):
        self.DEFINED_mid = mid
        self.DEFINED_INFO_HTTP_Headers = {
            'referer': f'https://space.bilibili.com/{self.DEFINED_mid}', 'user-agent': UserAgent}
        self.DEFINED_VIDEO_HTTP_Headers = {
            'referer': f'https://space.bilibili.com/{self.DEFINED_mid}/video', 'user-agent': UserAgent}
        self.DEFINED_ARTICLE_HTTP_Headers = {
            'referer': f'https://space.bilibili.com/{self.DEFINED_mid}/article', 'user-agent': UserAgent}
        
        self.DEFINED_info_url = f'https://api.bilibili.com/x/space/acc/info?mid={self.DEFINED_mid}'
        self.DEFINED_TotalVideo_url = f'https://api.bilibili.com/x/space/arc/search?mid={self.DEFINED_mid}&ps=1&order=pubdate'
        self.DEFINED_TotalArticle_url = f'https://api.bilibili.com/x/space/article?mid={self.DEFINED_mid}&pn=1&ps=12&sort=publish_time'

    @property
    def GetUpName(self):
        '''获取UP主用户名称'''
        return rget(self.DEFINED_info_url, headers = self.DEFINED_INFO_HTTP_Headers).json()['data']['name']
    @property
    def GetUpAvatar(self):
        '''获取UP主头像'''
        return rget(self.DEFINED_info_url, headers = self.DEFINED_INFO_HTTP_Headers).json()['data']['face']
    @property
    def GetUpDocument(self):
        '''获取UP主简介'''
        return rget(self.DEFINED_info_url, headers = self.DEFINED_INFO_HTTP_Headers).json()['data']['sign']
    @property
    def GetUpContent(self):
        '''获取UP主所有信息，以JSON形式输出'''
        return rget(self.DEFINED_info_url, headers = self.DEFINED_INFO_HTTP_Headers).json()

    @property
    def GetTotalVideo(self):
        '''获取UP主上传的视频总数'''
        return rget(self.DEFINED_TotalVideo_url, headers = self.DEFINED_VIDEO_HTTP_Headers).json()['data']['page']['count']
    @property
    def GetTotalArticle(self):
        '''获取UP主上传的专栏总数'''
        return rget(self.DEFINED_TotalArticle_url, headers = self.DEFINED_ARTICLE_HTTP_Headers).json()['data']['count']



