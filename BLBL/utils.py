from requests import get as rget, post as rpost
from threading import Thread
from lxml import etree
from time import sleep
from random import uniform as rand_float
from os import mkdir
from os.path import exists, isfile
import re

def fwrite(filePath, fileData):
    with open(filePath, 'wb') as f:
        f.write(fileData)
    return

def timeSleep(min_value = 0, max_value = None):
    sleep(rand_float(min_value, max_value))
