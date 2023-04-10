# pip install you-get
import subprocess

def run(cmd :str):
    subprocess.call(cmd, shell=True)

def download(url :str, outFolder :str = None, outFile :str = None):
    _command = f'you-get {url} -l'
    if outFolder:
        _command += f' -o {outFolder}'
    if outFile:
        _command += f' -O {outFile}'
    run(_command)

url = "https://www.bilibili.com/video/BV1Gq4y1g7B6"
out = '/media/sng/kdisk/哔哩哔哩下载/you_get'

download(url, outFolder=out)




