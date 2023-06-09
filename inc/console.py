#!/usr/bin/env python
# coding=utf-8
from inc import init
from inc import run, output, common, dnslog
import sys

def pocbomber_console():
    """控制台"""
    if common.get_value("dnslog_flag") and not common.get_value("target_list"):
        dnslog.dnslog_server()
        sys.exit()
    if common.get_value("dnslog_flag") and common.get_value("target_list"):
        dnslog.start_dnslog_scan()
    if common.get_value("delay"):
        common.set_value("max_threads", 1)
    if common.get_value("show"):
        output.show(common.get_value("script_list"))
        sys.exit()
    if not common.get_value("target_list"):
        output.usage()
        sys.exit()

    print('\n[*] starting {0}\n'.format(output.get_time1()))
    output.start_output()
    target_list = common.get_value("target_list")
    script_list = common.get_value("script_list")
    output.log_info('检测到 {0} 个目标, 已加载 {1} 条POC'.format(len(target_list), len(script_list)))
    run.verify(target_list, script_list)
    output.close_output()
    if common.get_value('attack'):
        output.log_info('检测到--attack参数, 开始尝试调用exp')
        if run.attack(target_list[0], script_list[0]):
            output.log_success('ATTACK END! enjoy : ) ')
        else:
            output.log_error('ATTACK FAIL! What\'s wrong?')

    print('\n[+] ending {0}\n'.format(output.get_time1()))

