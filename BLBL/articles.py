from .utils import *

def CreateFileName(PictureArchivePath :str, UID :str, link):
    """创建用来存档的文件名"""
    return PictureArchivePath + '/' + UID + '_' + \
    re.findall(r'https://[\w\d.]+/bfs/article/(?:\w+/)?([\d\w]+.\w+)', link, re.S | re.I)[0]

def CheckArchivePictureLinks(self, PictureArchivePath: str, PictureLinkArchiveFilePath :str = None):
    '''检查图片链接存档文件是否有问题，以及处理一些事情'''
    if PictureLinkArchiveFilePath: # 如果PictureLinkArchiveFilePath不为空
        if exists(PictureLinkArchiveFilePath): # 如果PictureLinkArchiveFilePathh指向的文件存在
            with open(PictureLinkArchiveFilePath, 'r', encoding='ascii') as f:
                try: # 用ASCII做编码格式检测文件是否合理
                    self.results_pictures_links = f.read().strip('\n').split('\n')
                except UnicodeDecodeError:
                    exit(f'>--< 请检查图片链接存档文件内容是否含有非英文字符')
        else: # 如果PictureLinkArchiveFilePathh指向的文件不存在
            exit(f'>--< 图片链接存档文件不存在，请检查！\n'
                f'>--< 图片链接存档文件路径: {PictureLinkArchiveFilePath}')
    else: # 如果PictureLinkArchiveFilePath为空，就从头获取图片链接
        self.GetLinksToAllPictures
    
    # 如果self.results_pictures_links为空
    if not self.results_pictures_links or not self.results_pictures_links[0]:
        exit(f'>--< 未获取到任何图片链接，请检查你的配置！\n'
            f'>--< UP主UID: {self.DEFINED_mid}\n'
            f'>--< 图片链接存档文件路径: {PictureLinkArchiveFilePath}\n'
            f'>--< 如果确认无误，请联系此程序开发者进行修复！')

    if not exists(PictureArchivePath): # 如果PictureArchivePath指向的目录不存在
        print(f'>--< 用于存档图片的目录不存在，将创建...')
        mkdir(PictureArchivePath)
    elif isfile(PictureArchivePath): # 如果PictureArchivePath指向的是文件
        exit(f'>--< 用于存档图片的路径不是文件夹！')

class article:
    '''帮助文档
    
    此类需要一个参数
        mid为UP主UID，是必需的。
    
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
        你可以使用保存的图片链接的那个txt文件来批量下载
        也可以从头开始获取专栏链接清洗出图片链接批量下载
        函数为 DownloadAllPictures
    关于杂项(垃圾)图片
        因为是下载指定UP主所有专栏中的所有图片
        所以难免可能会下载到一些你不想要的内容
        关于此问题的处理：
            图片保存完成之后，打开文件夹，排序方式：文件大小(从小到大)
            然后手动一个一个删除不需要的图片文件
        为什么不在代码内设置一个杂项(垃圾)图片过滤器：
            因为你下载的图片我并不能确定是什么样的
            所以直接添加这种功能可能会导致你所需要的图片被过滤掉
    '''
    def __init__(self, mid: str):
        self.DEFINED_mid = mid
        self.DEFINED_HTTP_Headers = { # 设定HTTP请求头
            'referer': f'https://space.bilibili.com/{self.DEFINED_mid}/article',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
        }

        self.PictureSize = 65536 # 过滤垃圾图片的文件大小阈值(单位: Bytes)
        self.results_article_links  = [] # 用来存放所有专栏的对应文章链接
        self.results_pictures_links = [] # 用来存放所有专栏中对应图片链接
        
        print(f'>>>> 此轮UP主UID: {self.DEFINED_mid}')
        try: re.findall(r"[^\d+]", self.DEFINED_mid, re.S | re.I)[0]; exit(f'>--< 错误UID，请勿含有非数字字符！')
        except IndexError: pass

    @property
    def GetLinksToAllArticles(self):
        '''获取指定up主的所有专栏的对应文章链接'''
        # 设定一个比较大的数以获取所有专栏，可以用while循环来做但是我不想
        for pn in range(1, 16777217):
            print(f'>>>> 正在获取专栏第{pn}页的内容...')
            url = f'https://api.bilibili.com/x/space/article?mid={self.DEFINED_mid}&pn={pn}&ps=12&sort=publish_time'
            res = rget(url, headers = self.DEFINED_HTTP_Headers).json()
            
            try: # 通过获取的数据的某一段长度来判断专栏是否爬取完毕
                if len(res['data']) == 3: print(f'>>>> 获取完毕.'); break
            except KeyError: exit(f'>--< 请检查UID是否正确或此UP主是否发布过专栏！')
            
            # 每一个json数据里有最多12个专栏的id，将这些id与网址拼接起来存入变量
            for index in range(len(res['data']['articles'])):
                self.results_article_links.append(f"https://www.bilibili.com/read/cv{res['data']['articles'][index]['id']}")

    @property
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
            try: # 为单个图片文件命名，使用UP主UID与图片h本身的SHA1值名
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

