#!/usr/bin/env python
# coding=utf-8
from inc import init
from inc import thread, common
# 禁用https报错
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)


def verify(target_list, script_list):
    thread_pool = thread.ThreadPool()
    for current_target in target_list:
        [thread_pool.add_task(current_target, script) for script in script_list]         # 向线程池中添加所有poc和当前的url
    thread_pool.start_threadpool()

def attack(target, script):
    try:
        if common.get_value("pocinfo_dict")[script].attack(target):
            return True
        return False
    except:
        return False








