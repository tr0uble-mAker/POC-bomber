#!/usr/bin/env python
# coding=utf-8

##########################################################
#   Thinkphp框架漏洞检测模块(包含多个互联网已知poc，部分poc带有exp模块)
#   此模块可单独调用检测Thinkphp漏洞
#   thinkphp()公共函数可被其他模块调用
##########################################################

# 加载POC
from pocs.framework.thinkphp.thinkphp32x_rce import thinkphp32x_rce
from pocs.framework.thinkphp.thinkphp2_rce import thinkphp2_rce
from pocs.framework.thinkphp.thinkphp5_sqli import thinkphp5_sqli
from pocs.framework.thinkphp.thinkphp5022_5129 import thinkphp5022_5129_rce
from pocs.framework.thinkphp.thinkphp5023_rce import thinkphp5023_rce
from pocs.framework.thinkphp.thinkphp_driver_display_rce import thinkphp_driver_display_rce
from pocs.framework.thinkphp.thinkphp_index_construct_rce import thinkphp_index_construct_rce
from pocs.framework.thinkphp.thinkphp_index_showid_rce import thinkphp_index_showid_rce
from pocs.framework.thinkphp.thinkphp_invoke_func_code_exec import thinkphp_invoke_func_code_exec
from pocs.framework.thinkphp.thinkphp_lite_code_exec import thinkphp_lite_code_exec
from pocs.framework.thinkphp.thinkphp_method_filter_code_exec import thinkphp_method_filter_code_exec
from pocs.framework.thinkphp.thinkphp_multi_sql_leak import thinkphp_multi_sql_leak
from pocs.framework.thinkphp.thinkphp_pay_orderid_sqli import thinkphp_pay_orderid_sqli
from pocs.framework.thinkphp.thinkphp_request_input_rce import thinkphp_request_input_rce
from pocs.framework.thinkphp.thinkphp_timebased_sqli import thinkphp_timebased_sqli
from pocs.framework.thinkphp.thinkphp_view_recent_xff_sqli import thinkphp_view_recent_xff_sqli
from inc import output, run
import re

def thinkphp():          # 返回poc检测函数字符串列表
    poclist = [
        'thinkphp32x_rce',
        'thinkphp2_rce',
        'thinkphp5_sqli',
        'thinkphp5022_5129_rce',
        'thinkphp5023_rce',
        'thinkphp_driver_display_rce',
        'thinkphp_index_construct_rce',
        'thinkphp_index_showid_rce',
        'thinkphp_invoke_func_code_exec',
        'thinkphp_lite_code_exec',
        'thinkphp_method_filter_code_exec',
        'thinkphp_multi_sql_leak',
        'thinkphp_pay_orderid_sqli',
        'thinkphp_request_input_rce',
        # 'thinkphp_timebased_sqli',
        'thinkphp_view_recent_xff_sqli',
    ]
    return poclist



