#!/usr/bin/env python
# coding=utf-8

# 全局poc执行模块

# 加载全局poc
from inc.init import *
from inc.thread import *
# 忽略https报错
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)


def run(url, threads_num=1):
    report = []
    threads = Threads(threads_num)
    pocmodel = get_pocmodel(url)
    for poclist in pocmodel:
        for poc in poclist:
            if threads_num == 1:
                relsult = eval(poc)
                print('\n[+] 正在检测: ', str(relsult['name']))
                if relsult['vulnerable']:
                    report.append(relsult)
                    print('\n[@] 检测到漏洞:', relsult['name'])
            else:
                threads.add_task(poc)
    if threads_num > 1:
        threads.start_thread()
        report = threads.get_report()
    return report



