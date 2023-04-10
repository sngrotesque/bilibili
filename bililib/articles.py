from threading import Thread
from lxml import etree
from .utils import *

class article:
    '''\
    此类需要一个参数
        mid为UP主UID，是必需的。
    
    关于爬取专栏链接
        此程序将按照UP主的发布时间排序以爬取专栏
        也就是从新到旧的爬取
        函数为 GetLinksToAllArticles
        爬取结果存入类中results_article_links变量
    '''
    def __init__(self, mid: str):
        self.DEFINED_mid = mid
        self.DEFINED_HTTP_Headers = {
            'referer': f'https://space.bilibili.com/{self.DEFINED_mid}/article',
            'user-agent':UserAgent}

        self.PictureSize = 65536 # 过滤垃圾图片的文件大小阈值(单位: Bytes)
        self.results_article_links  = [] # 用来存放所有专栏的对应文章链接
        self.results_pictures_links = [] # 用来存放所有专栏中对应图片链接

    @property
    def GetLinksToAllArticles(self):
        '''获取指定up主的所有专栏的对应文章链接'''
        # 设定一个比较大的数以获取所有专栏，可以用while循环来做但是我不想
        for pn in range(1, 16777217):
            print(f'>>>> 正在获取专栏第{pn}页的内容...')
            url = f'https://api.bilibili.com/x/space/article?mid={self.DEFINED_mid}&pn={pn}&ps=12&sort=publish_time'
            res = rget(url, headers = self.DEFINED_HTTP_Headers).json()
            
            try:
                # 通过获取的数据的某一段长度来判断专栏是否爬取完毕
                res['data']['articles']
                if len(res['data']) == 3:
                    print(f'>>>> 获取完毕.')
                    break
            except KeyError:
                exit(f'>--< 请检查UID是否正确或此UP主是否发布过专栏！')
            
            # 每一个json数据里有最多12个专栏的id，将这些id与网址拼接起来存入变量
            for index in range(len(res['data']['articles'])):
                self.results_article_links.append(f"https://www.bilibili.com/read/cv{res['data']['articles'][index]['id']}")

    def GetLinksToAllPictures(self):
        '''获取指定up主的所有专栏的对应图片链接(获取所有的文章链接，然后通过专栏链接获取内部所有图片链接)'''
        self.GetLinksToAllArticles
        for article_url in self.results_article_links:
            print(f'>>>> 正在获取{article_url}中所有图片链接.')
            articlePicturesHTML = rget(article_url, headers = self.DEFINED_HTTP_Headers).text
            articlePicturesHTML = etree.HTML(articlePicturesHTML).xpath(
            '/html/body/div/div/div/div/div/div/figure/img/@data-src')
            for articlePictureLink in articlePicturesHTML:
                if 'https:' not in articlePictureLink: articlePictureLink = f'https:{articlePictureLink}'
                self.results_pictures_links.append(articlePictureLink)

    def DownloadAllPictures(self, PictureArchivePath :str, PictureLinkArchiveFilePath :str = None):
        '''将图片存档至用户指定的目录中，如果目录不存在将创建
        可使用变量PictureLinkArchiveFilePath来指定读取用于存放图片链接的文件'''
        CheckArchivePictureLinks(self, PictureArchivePath, PictureLinkArchiveFilePath)

        NumberOfPicturesSaved = 1 # 用作标注当前是第几个图片
        for link in self.results_pictures_links:
            try: # 为单个图片文件命名，使用UP主UID与图片本身的SHA1值名
                PictureFilePath = CreateFileName(PictureArchivePath, self.DEFINED_mid, link)
            except IndexError: # 因为部分图片链接中会有B站动图的GIF文件，所以采取过滤机制，并开始下载下一张图片
                print(f'>>>> {NumberOfPicturesSaved:0>4} {link}非正常图片，跳过...')
                NumberOfPicturesSaved += 1; continue
            if exists(PictureFilePath):
                # 如果存档路径存在同名文件则跳过，主要用在使用此库时突然退出的情况，并开始下载下一张图片
                print(f'>>>> {NumberOfPicturesSaved:0>4} {PictureFilePath}已存在，跳过...')
                NumberOfPicturesSaved += 1; continue
            
            PictureData = rget(link, headers = self.DEFINED_HTTP_Headers).content
            if len(PictureData) < self.PictureSize: # 如果图片小于self.PictureSize设定的值就处理下一张
                print(f'>>>> {NumberOfPicturesSaved:0>4} {link}图片过小: {len(PictureData)} Bytes，忽略...')
                NumberOfPicturesSaved += 1; continue
            
            fwrite(PictureFilePath, PictureData)
            print(f'>>>> {NumberOfPicturesSaved:0>4} 已保存图片: {link[-44:]}')
            NumberOfPicturesSaved += 1

    def MultiThreadDownloadPictures(self, PictureArchivePath :str, PictureLinkArchiveFilePath :str = None):
        '''使用多线程下载图片(默认8线程)，参数使用方法同DownloadAllPictures函数'''
        CheckArchivePictureLinks(self, PictureArchivePath, PictureLinkArchiveFilePath)
        
        def ThreadDownload(pictures_links_list :list, ThreadSerialNumber :int, Number_of_threads :int):
            for _ in range(len(pictures_links_list) // Number_of_threads):
                link = pictures_links_list[ThreadSerialNumber] # 将变量名统一
                
                try: # 为单个图片文件命名，使用UP主UID与图片h本身的SHA1值名
                    PictureFilePath = CreateFileName(PictureArchivePath, self.DEFINED_mid, link)
                except IndexError: # 因为部分图片链接中会有B站动图的GIF文件，所以采取过滤机制，并开始下载下一张图片
                    print(f'>>>> {ThreadSerialNumber+1:0>4} {link}非正常图片，跳过...')
                    ThreadSerialNumber += Number_of_threads; continue
                if exists(PictureFilePath):
                    # 如果存档路径存在同名文件则跳过，主要用在使用此库时突然退出的情况，并开始下载下一张图片
                    print(f'>>>> {ThreadSerialNumber+1:0>4} {PictureFilePath}已存在，跳过...')
                    ThreadSerialNumber += Number_of_threads; continue

                PictureData = rget(link, headers = self.DEFINED_HTTP_Headers).content
                if len(PictureData) < self.PictureSize: # 如果图片小于self.PictureSize设定的值就处理下一张
                    print(f'>>>> {ThreadSerialNumber+1:0>4} {link}图片过小: {len(PictureData)} Bytes，忽略...')
                    ThreadSerialNumber += Number_of_threads; continue

                fwrite(PictureFilePath, PictureData)
                print(f'>>>> {ThreadSerialNumber+1:0>4} 已保存图片: {link[-44:]}')
                ThreadSerialNumber += Number_of_threads
        
        # 开始调用MultiThreadDownload函数，创建Number_of_threads个线程
        Number_of_threads = 8
        th = [Thread(target = ThreadDownload, args = (self.results_pictures_links, x, Number_of_threads))
            for x in range(Number_of_threads)]
        for x in th: x.start()
        for x in th: x.join()

        # 多线程执行完毕之后检测是否存在遗漏
        TotalPictureLinks = len(self.results_pictures_links)
        url_residue = TotalPictureLinks % Number_of_threads
        for index in range(TotalPictureLinks - url_residue, TotalPictureLinks):
            link = self.results_pictures_links[index] # 将变量名统一
            try: # 为单个图片文件命名，使用UP主UID与图片h本身的SHA1值名
                PictureFilePath = CreateFileName(PictureArchivePath, self.DEFINED_mid, link)
            except IndexError: # 因为部分图片链接中会有B站动图的GIF文件，所以采取过滤机制，并开始下载下一张图片
                print(f'>>>> {index+1:0>4} {link}非正常图片，跳过...')
                continue
            if exists(PictureFilePath):
                # 如果存档路径存在同名文件则跳过，主要用在使用此库时突然退出的情况，并开始下载下一张图片
                print(f'>>>> {index+1:0>4} {PictureFilePath}已存在，跳过...')
                continue
            PictureData = rget(link, headers = self.DEFINED_HTTP_Headers).content
            if len(PictureData) < self.PictureSize: # 如果图片小于self.PictureSize设定的值就处理下一张
                print(f'>>>> {index+1:0>4} {link}图片过小: {len(PictureData)} Bytes，忽略...')
                continue
            fwrite(PictureFilePath, PictureData)
            print(f'>>>> {index+1:0>4} 已保存图片: {link[-44:]}')

