#!/usr/bin/env python
# coding=utf-8

# 此模块加载全局poc
# 将漏洞分为四个模块分别为 框架漏洞 中间件漏洞 常见端口漏洞 web页面漏洞

from pocs.framework.main import *
from pocs.middleware.main import *
from pocs.ports.main import *
from pocs.web.main import *

def get_pocmodel(url):
    pocmodel = []
    pocmodel.append(framework(url))
    pocmodel.append(middleware(url))
    pocmodel.append(ports(url))
    pocmodel.append(web(url))

    return pocmodel