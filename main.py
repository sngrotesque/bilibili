import BLBL

up_uid_list = [
    '389328307',
    '12073864',
    '355576491'
]

# 单线程下载图片
# up_mid                     = '389328307' # UP主的UID，不知道如何获取的话请百度
# PictureLinkArchiveFilePath = 'p:/bilibili_389328307_原神某网站的奇怪同人图.txt' # 保存有图片链接的文件路径（留空就视为从头开始爬取）
# PictureArchivePath         = 'p:/bilibili_389328307_原神某网站的奇怪同人图' # 用于保存下载的图片的文件夹

# res = BLBL.article(up_mid)
# res.DownloadAllPictures(PictureArchivePath, PictureLinkArchiveFilePath)

# 多线程下载图片
up_mid                     = '389328307' # UP主的UID，不知道如何获取的话请百度
PictureLinkArchiveFilePath = './url.txt' # 保存有图片链接的文件路径（留空就视为从头开始爬取）
PictureArchivePath         = 'bilibili_389328307_原神某网站的奇怪同人图' # 用于保存下载的图片的文件夹

res = BLBL.article(up_mid)
res.MultiThreadDownloadPictures(PictureArchivePath, PictureLinkArchiveFilePath)

# 测试使用
# up_mid = '389328307'
# res = BLBL.article(up_mid)

# res.DownloadAllPictures('p:/bilibili_389328307_原神某网站的奇怪同人图')
