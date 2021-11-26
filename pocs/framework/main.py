#!/usr/bin/env python
# coding=utf-8


from pocs.framework.struct2.main import *
from pocs.framework.thinkphp.main import *


def framework(url):
    print('\n[+] 正在加载 开发框架漏洞 poc检测模块......')
    poclist = []
    poclist = poclist + struct2(url)
    poclist = poclist + thinkphp(url)


    return poclist


