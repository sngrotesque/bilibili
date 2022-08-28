from requests import get as rget
from lxml import etree
from time import sleep
from random import uniform as rand_float
from os import mkdir
from os.path import exists, isfile
import re

def temp_var(uid = None):
    389328307
    12073864
    355576491

class article:
    '''帮助文档
    
    此类需要两个参数
        mid与MaximumTimeOfRandomSleep
    mid为UP主UID，是必需的。
    MaximumTimeOfRandomSleep为随机休眠的最长时间，用于规避哔哩哔哩的反爬虫机制。
    
    关于爬取专栏链接
        此程序将按照UP主的发布时间排序以爬取专栏
        也就是从新到旧的爬取
        函数为 GetLinksToAllArticles
        爬取结果存入类中results_article_links变量
    关于爬取图片链接
        这个问题，只存在于获取专栏图片链接的时候。
        如果你执行的是下载保存图片的步骤，那么就不会有这个问题。
        在爬取图片的过程中，难免会爬取到b站的分割线UI
        为什么？因为那堆分割线并不是字符而是图片。
        一些UP主在专栏会添加分割线，没办法。
        函数为 GetLinksToAllPictures
        爬取结果存入类中results_pictures_links变量
    关于下载图片
        下载时程序会忽略掉小于32kb的图片(因为极有可能是B站的UI图片)
        使用requests库的get类中的content方法
        
        你可以使用保存的图片链接的那个txt文件来批量下载
        也可以从头开始获取专栏链接清洗出图片链接批量下载
        函数为 DownloadAllPictures
    '''
    def __init__(self, mid: str, MaximumTimeOfRandomSleep :float = 0):
        self.DEFINED_mid = mid
        self.DEFINED_MaximumTimeOfRandomSleep = MaximumTimeOfRandomSleep
        self.DEFINED_HTTP_Headers = { # 设定HTTP请求头
            'referer': f'https://space.bilibili.com/{self.DEFINED_mid}/article',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
        }

        self.results_article_links = [] # 用来存放所有专栏的对应文章链接
        self.results_pictures_links = [] # 用来存放所有专栏中对应图片链接
        
        print(f'>>>> 此轮UP主UID: {self.DEFINED_mid}')
        try:
            re.findall(r"[^\d+]", self.DEFINED_mid, re.S | re.I)[0]
            exit(f'>--< 错误UID，请勿含有非数字字符！')
        except IndexError:
            pass

    @property
    def GetLinksToAllArticles(self):
        '''获取指定up主的所有专栏的对应文章链接
        '''
        # 设定一个比较大的数以获取所有专栏，可以用while循环来做但是我不想
        for pn in range(1, 65536):
            print(f'>>>> 正在获取专栏第{pn}页的内容...')
            url = f'https://api.bilibili.com/x/space/article?mid={self.DEFINED_mid}&pn={pn}&ps=12&sort=publish_time'
            res = rget(url, headers = self.DEFINED_HTTP_Headers).json()
            
            # 通过获取的数据的某一段长度来判断专栏是否爬取完毕
            try:
                if len(res['data']) == 3: print(f'>>>> 获取完毕.'); break
            except KeyError:
                exit(f'>--< 请检查UID是否正确或此UP主是否发布过专栏！')
            
            # 每一个json数据里有最多12个专栏的id
            # 将这些id与网址拼接起来存入变量
            for x in range(len(res['data']['articles'])):
                self.results_article_links.append(f"https://www.bilibili.com/read/cv{res['data']['articles'][x]['id']}")
                
                # 随机休眠一段时间，模拟人类访问
                sleep(rand_float(0, self.DEFINED_MaximumTimeOfRandomSleep))

    @property
    def GetLinksToAllPictures(self):
        '''获取指定up主的所有专栏的对应图片链接
        '''
        self.GetLinksToAllArticles # 获取所有的文章链接
        
        # 在self.PictureLinkDirectoryName目录中创建一个文件用来写入图片的链接
        for url in self.results_article_links:
            print(f'>>>> 正在获取{url}中所有图片链接...')
            res = rget(url, headers = self.DEFINED_HTTP_Headers).text
            res = etree.HTML(res).xpath('/html/body/div/div/div/div/div/div/figure/img/@data-src')
            print(f'>>>> 已获取{len(res)}个图片链接.')
            for link in res:
                if 'https:' not in link: link = f'https:{link}'
                self.results_pictures_links.append(link)

    def DownloadAllPictures(self, PictureArchivePath :str, PictureLinkArchiveFilePath :str = None):
        '''将图片存档至用户指定的目录中，如果目录不存在将创建
        可使用变量PictureLinkArchiveFilePath来指定读取用于存放图片链接的文件
        '''
        if PictureLinkArchiveFilePath:
            if exists(PictureLinkArchiveFilePath):
                with open(PictureLinkArchiveFilePath, 'r', encoding='ascii') as f:
                    try:
                        self.results_pictures_links = f.read().strip('\n').split('\n')
                    except UnicodeDecodeError:
                        exit(f'>--< 请检查图片链接存档文件内容是否含有非英文字符')
            else:
                exit(f'>--< 图片链接存档文件不存在，请检查！\n'
                    f'>--< 图片链接存档文件路径: {PictureLinkArchiveFilePath}')
        else: self.GetLinksToAllPictures
        if not self.results_pictures_links or not self.results_pictures_links[0]:
            exit(f'>--< 未获取到任何图片链接，请检查你的配置！\n'
                f'>--< UP主UID: {self.DEFINED_mid}\n'
                f'>--< 图片链接存档文件路径: {PictureLinkArchiveFilePath}\n'
                f'>--< 如果确认无误，请联系此程序开发者进行修复！')

        if not exists(PictureArchivePath):
            print(f'>--< 用于存档图片的目录不存在，将创建...')
            mkdir(PictureArchivePath)
        elif isfile(PictureArchivePath):
            exit(f'>--< 用于存档图片的路径不是文件夹！')

        # 图片大小阈值，小于此大小会被忽略，用于过滤垃圾图片
        PictureSize = 64 * 1024 ** 1

        for link in self.results_pictures_links:
            # 为单个图片文件命名
            PictureFilePath = PictureArchivePath + '/' + self.DEFINED_mid + '_' + re.findall(
                r'https://[\w\d.]+/bfs/article/'
                r'(?:\w+/)?'
                r'([\d\w]+.\w+)', link, re.S | re.I)[0]
            if exists(PictureFilePath):
                print(f'>>>> {PictureFilePath}已存在，跳过...')
                continue
            
            # 下载图片用于存档
            PictureData = rget(link, headers = self.DEFINED_HTTP_Headers).content
            if len(PictureData) < PictureSize:
                print(f'>>>> {link}图片过小: {len(PictureData)} Bytes，忽略...')
                continue
            
            # 确保没有垃圾图片与重名文件的话就保存数据至文件
            with open(PictureFilePath, 'wb') as f:
                f.write(PictureData)
                print(f'>>>> 已保存图片: {link}')

