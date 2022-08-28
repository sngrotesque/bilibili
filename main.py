import BLBL
import ssl

up_mid                     = '12073864' # UP主的UID，不知道如何获取的话请百度
PictureLinkArchiveFilePath = '' # 保存有图片链接的文件路径（留空就视为从头开始爬取）
PictureArchivePath         = 'bilibili_12073864_明日方舟图片分享' # 用于保存下载的图片的文件夹

res = BLBL.article(up_mid)
res.DownloadAllPictures(PictureArchivePath, PictureLinkArchiveFilePath)



