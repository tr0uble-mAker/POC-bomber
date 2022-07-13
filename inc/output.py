#!/usr/bin/env python
# coding=utf-8

VERSION = '2.03'

import random, time, os, sys

def get_time1():
    return time.strftime("@ %Y-%m-%d /%H:%M:%S/", time.localtime())

def get_time2():
    return time.strftime("%H:%M:%S", time.localtime())

def output(thread_pool, futures, ouput_path=''):
    succeed_report = []
    for future in futures:
        try:
            current_target = thread_pool.futures[future]
            relsult = future.result()
            if relsult['vulnerable']:
                status_print('检测到: {0}  目标: {1} !'.format(relsult['name'], current_target), 1)
                succeed_report.append(relsult)
                if ouput_path != '':
                    data_save(ouput_path, relsult)
            else:
                status_print('正在检测: [{0}]  poc: {1}'.format(current_target, relsult['name']), 0)
        except:
            status_print('poc中产生一个错误', 2)
            pass
    status_print('所有检测任务完成, 即将生成报告......', 0)
    if len(succeed_report) != 0:
        print('----')
        for relsult in succeed_report:
            first = True
            for r in relsult:
                if first:
                    value = '[!] {0}: {1}'.format(str(r.capitalize()), str(relsult[r]))
                    status_print(value, 4)
                    first = False
                else:
                    value = '     {0}: {1}'.format(str(r.capitalize()), str(relsult[r]))
                    status_print(value, 4)
        print('----')
        if ouput_path != '':
            status_print('已将报告写入至 {0} !'.format(os.path.join(os.path.abspath('.'), ouput_path)), 0)
        else:
            status_print('程序没有生成任何报告类文件以记录此次任务的数据', 2)
    else:
        status_print('所有测试已结束但是程序未生成任何报告', 3)


def data_save(output_path, relsult):
    report_file = open(output_path, 'a+')
    value = ''
    for r in relsult.keys():
        if str(r) == 'name':
            value += '[!] {0}: {1}\n'.format(str(r.capitalize()), relsult['name'])
        else:
            value += '     {0}: {1}\n'.format(str(r.capitalize()), relsult[r])
    report_file.write(value)
    report_file.close()



def logo():
    logo0 = r'''
    
    
 ____   ___   ____   ____                  _               
|  _ \ / _ \ / ___| | __ )  ___  _ __ ___ | |__   ___ _ __ 
| |_) | | | | |     |  _ \ / _ \| '_ ` _ \| '_ \ / _ \ '__|
|  __/| |_| | |___  | |_) | (_) | | | | | | |_) |  __/ |   
|_|    \___/ \____| |____/ \___/|_| |_| |_|_.__/ \___|_|   

    
    
                                                Version {0}
                                                            Author  tr0uble_mAker
                                                            Whoami  https://github.com/tr0uble-mAker
'''
    print(logo0.format(VERSION))


def usage():
    print('''
        用法:
                获取poc/exp信息:   python3 pocbomber.py --show
                单目标检测:        python3 pocbomber.py -u http://xxx.xxx.xx 
                批量检测:          python3 pocbomber.py -f url.txt -o report.txt
                指定poc检测:       python3 pocbomber.py -f url.txt --poc="thinkphp2_rce.py"
                exp攻击模式:       python3 pocbomber.py -u 目标url --poc="指定poc文件" --attack
        参数:
                -u  --url      目标url
                -f  --file     指定目标url文件   
                -o  --output   指定生成报告的文件(默认不生成报告)
                -p  --poc      指定单个或多个poc进行检测, 直接传入poc文件名, 多个poc用(,)分开
                -t  --thread   指定线程池最大并发数量(默认300)
                --show         展示poc/exp详细信息
                --attack       使用poc文件中的exp进行攻击
                --dnslog       使用dnslog平台检测无回显漏洞(默认不启用dnslog,可在配置文件中默认启用)''', end='')

import platform
if 'Windows' in platform.system():
    import ctypes, sys
    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12

    # 字体颜色定义 text colors
    FOREGROUND_BLUE = 0x09  # blue.
    FOREGROUND_GREEN = 0x0a  # green.
    FOREGROUND_DEEPGREEN = 0x02 # dark green.
    FOREGROUND_RED = 0x0c  # red.
    FOREGROUND_YELLOW = 0x0e  # yellow.
    FOREGROUND_WHITE = 0x0f  # white.

    # get handle
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    def set_cmd_text_color(color, handle=std_out_handle):
        Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return Bool
    # reset white
    def resetColor():
        set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

    # green
    def printGreen(mess):
        set_cmd_text_color(FOREGROUND_GREEN)
        sys.stdout.write(mess)
        sys.stdout.flush()
        resetColor()

    # red
    def printRed(mess):
        set_cmd_text_color(FOREGROUND_RED)
        sys.stdout.write(mess)
        sys.stdout.flush()
        resetColor()

    # yellow
    def printYellow(mess):
        set_cmd_text_color(FOREGROUND_YELLOW)
        sys.stdout.write(mess)
        sys.stdout.flush()
        resetColor()

    def printDeepGreen(mess):
        set_cmd_text_color(FOREGROUND_DEEPGREEN)
        sys.stdout.write(mess)
        sys.stdout.flush()
        resetColor()

    def printBlue(mess):
        set_cmd_text_color(FOREGROUND_BLUE)
        sys.stdout.write(mess)
        sys.stdout.flush()
        resetColor()

    def printWhite(mess):
        set_cmd_text_color(FOREGROUND_WHITE)
        sys.stdout.write(mess + '\n')
        sys.stdout.flush()
        resetColor()

    def get_INFO():
        printBlue('[{0}] '.format(get_time2()))
        printDeepGreen('[INFO] ')

    def get_SUCCESS():
        printBlue('[{0}] '.format(get_time2()))
        printGreen('[SUCCESS] ')

    def get_WARNING():
        printBlue('[{0}] '.format(get_time2()))
        printYellow('[WARNING] ')

    def get_CRITICAL():
        printBlue('[{0}] '.format(get_time2()))
        printRed('[CRITICAL] ')

else:
    DEEP_GREEN = "\033[30;1m{0}\033[0m"
    GREEN = "\033[32;1m{0}\033[0m"
    WHITE = "\033[29;1m{0}\033[0m"
    RED = "\033[31;1m{0}\033[0m"
    YELLOW = "\033[33;1m{0}\033[0m"
    BLUE = "\033[34;1m{0}\033[0m"

    def get_INFO():
        print('{0} {1} '.format(BLUE.format('[' + get_time2() + ']'), DEEP_GREEN.format('[INFO]')), end='')


    def get_SUCCESS():
        print('{0} {1} '.format(BLUE.format('[' + get_time2() + ']'), GREEN.format('[SUCCESS]')), end='')

    def get_WARNING():
        print('{0} {1} '.format(BLUE.format('[' + get_time2() + ']'), YELLOW.format('[WARNING]')), end='')

    def get_CRITICAL():
        print('{0} {1} '.format(BLUE.format('[' + get_time2() + ']'), RED.format('[CRITICAL]')), end='')

    def printWhite(mess):
        print('{0}'.format(WHITE.format(mess)))


def status_print(value='', status=-1):        # 日志输出函数
    if status == -1:                      # 默认输出       status = -1 (default)
        print(value)
    elif status == 0:                     # INFO         status = 0
        get_INFO()
        print(value)
    elif status == 1:                     # SUCCESS      status = 1
        get_SUCCESS()
        printWhite(value)
    elif status == 2:                     # WARNING      status = 2
        get_WARNING()
        print(value)
    elif status == 3:                     # CRITICAL     status = 4
        get_CRITICAL()
        print(value)
    elif status == 4:                     # 加粗          status = 5
        printWhite(value)

def show(poc_modole_list):
    poc_info_list = []
    exp_num = 0
    status_print('loading POC/EXP ......', 0)
    for poc_modole in poc_modole_list:
        path = poc_modole.__file__
        try:
            relsult = poc_modole.verify('http://0.0.0.0')
            name = relsult['name']
        except:
            continue
        try:
            attack = relsult['attack']
            exp_num += 1
        except:
            attack = False
        poc_info = (name, path, attack)
        poc_info_list.append(poc_info)

    for (name, path, attack) in poc_info_list:
        if 'Windows' in platform.system():
            if attack:
                printGreen('\n[+] Name: {0}         Attack: True\n'.format(name))
            else:
                printDeepGreen('\n[+] Name: {0}\n'.format(name))
            print('    Script: {0}'.format(path.split('\\')[-1]))
            print('    Path: {0}'.format(path))
        else:
            if attack:
                print('\n{0}\n'.format(GREEN.format('[+] Name: {0}         Attack: True'.format(name))), end='')
            else:
                print('\n{0}\n'.format(DEEP_GREEN.format('[+] Name: {0}'.format(name))), end='')
            print('    Script: {0}'.format(path.split('/')[-1]))
            print('    Path: {0}'.format(path))
    print('''\n\t\t\t\t\t\t\t\t\t\tTotal     POC: {0}    EXP: {1}'''.format(len(poc_info_list), exp_num))
