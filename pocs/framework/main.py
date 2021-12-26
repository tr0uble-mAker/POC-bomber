#!/usr/bin/env python
# coding=utf-8


from pocs.framework.struct2.main import *
from pocs.framework.thinkphp.main import *


def framework():
    poclist = []
    poclist = poclist + struct2()
    poclist = poclist + thinkphp()


    return poclist


