import BLBL


import requests

url = 'http://cn.bing.com/'
proxy = {"http":"http://20.24.22.143:8000","https":"http://20.24.22.143:8000"}
headers = {"User-Agent":"Mozilla/5.0 (X11; Linux i686; rv:97.0) Gecko/20100101 Firefox/97.0"}

res = requests.get(url, headers = headers, proxies = proxy)

print(res.text)

