#!/usr/bin/env python
# coding=utf-8

# 此模块加载全局poc
# 将漏洞分为四个模块分别为 框架漏洞 中间件漏洞 常见端口漏洞 web页面漏洞

from pocs.framework.main import *
from pocs.middleware.main import *
from pocs.ports.main import *
from pocs.web.main import *

def get_poc_list():
    poclist = []
    poclist += framework()
    poclist += middleware()
    poclist += ports()
    poclist += web()

    return poclist

