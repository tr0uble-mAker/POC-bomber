#!/usr/bin/env python
# coding=utf-8

# 全局poc执行模块

# 加载全局poc
from inc.init import *
from inc import config, thread, output


import time
# 忽略https报错
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)


def verify(target_list, poc_modole_list, output_path):
    try:
        thread_pool = thread.ThreadPool(config.max_thread)
        for current_target in target_list:
            [thread_pool.add_task(poc.verify, current_target) for poc in poc_modole_list]         # 向线程池中添加所有poc和当前的url

        futures = thread_pool.start_threadpool()
        output.output(thread_pool, futures, output_path)
        return True
    except:
        return False


def attack(target, poc_modole):
    try:
        if poc_modole.attack(target):
            return True
        else:
            return False
    except:
        return False








