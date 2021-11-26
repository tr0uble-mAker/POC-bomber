#!/usr/bin/env python
# coding=utf-8

from pocs.middleware.apache.main import *
from pocs.middleware.weblogic.main import *


def middleware(url):
    print('\n[+] 正在加载 中间件漏洞 poc检测模块......')
    poclist = []
    poclist = poclist + weblogic(url)
    poclist = poclist + apache(url)


    return poclist