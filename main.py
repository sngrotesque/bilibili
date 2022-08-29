import BLBL


# 单线程下载图片
# up_mid                     = '389328307' # UP主的UID，不知道如何获取的话请百度
# PictureLinkArchiveFilePath = 'p:/bilibili_389328307_原神某网站的奇怪同人图.txt' # 保存有图片链接的文件路径（留空就视为从头开始爬取）
# PictureArchivePath         = 'p:/bilibili_389328307_原神某网站的奇怪同人图' # 用于保存下载的图片的文件夹

# res = BLBL.article(up_mid)
# res.DownloadAllPictures(PictureArchivePath, PictureLinkArchiveFilePath)

# 多线程下载图片
# up_mid                     = '389328307' # UP主的UID，不知道如何获取的话请百度
# PictureLinkArchiveFilePath = './url.txt' # 保存有图片链接的文件路径（留空就视为从头开始爬取）
# PictureArchivePath         = 'bilibili_389328307_原神某网站的奇怪同人图' # 用于保存下载的图片的文件夹

# res = BLBL.article(up_mid)
# res.PicturesMultiThreadDownload(PictureArchivePath, PictureLinkArchiveFilePath)

# 测试使用
a = BLBL.articles.CreateFileName('bilibili_389328307_原神某网站的奇怪同人图', '389328307', 'https://i0.hdslb.com/bfs/article/f6a2297f63ed5cd20c55505e0c1acbc3d2d74f7c.jpg')
print(a)

