from requests import get as rget
from os.path import exists, isfile
from random import uniform
from time import sleep
from os import mkdir
import hashlib
import re

UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
Referer = 'https://www.bilibili.com/'

def fwrite(filePath, fileData):
    with open(filePath, 'wb') as f:
        f.write(fileData)
    return

def fread(filePath :str):
    with open(filePath, 'rb') as f:
        return f.read()

def checkFolder(dirPath :str):
    if not dirPath:
        print(f'>--< {dirPath}不存在，将创建。')
        mkdir(dirPath)

def timeSleep(min_value = 0, max_value = None):
    sleep(uniform(min_value, max_value))

def RequestGet(self, url :str):
    return rget(url, headers = self.HEADERS)

def sha256(data :object):
    hash = hashlib.sha256()
    hash.update(data)
    return hash.hexdigest()

def CreateFileName(PictureArchivePath :str, UID :str, link):
    # 创建用来存档的文件名
    return PictureArchivePath + '/' + UID + '_' + \
    re.findall(r'https://[\w\d.]+/bfs/article/(?:\w+/)?([\d\w]+.\w+)', link, re.S | re.I)[0]

def CheckArchivePictureLinks(self, PictureArchivePath: str, PictureLinkArchiveFilePath :str = None):
    # 检查图片链接存档文件是否有问题，以及处理一些事情
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
