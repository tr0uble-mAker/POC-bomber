#!/usr/bin/env python
# coding=utf-8

from inc import run, init, output, config
import argparse, sys, time

# POC bomber 控制台        参数处理和程序调用
def pocbomber_console(args):
    poc_modole_list = init.get_poc_modole_list()
    target_list = []
    if args.output:                             # --output
        config.output_path = args.output
    if args.thread:                             # --thread
        config.max_thread = args.thread
    if args.dnslog:                             # --dnslog
        config.dnslog_flag = True
    if args.poc:                                # --poc
        poc_modole_list = []
        for each_poc in args.poc.split(','):
            one_poc_modole = init.get_one_poc_modole(each_poc)
            if one_poc_modole:
                output.status_print('成功检测到poc文件: {0}'.format(one_poc_modole[1]), 0)
                poc_modole_list.append(one_poc_modole[0])
            else:
                output.status_print('未检测到poc文件: {0} '.format(each_poc), 2)

    if args.url and args.file is None:          # --url
        target_list.append(args.url)
    elif args.file and args.url is None:        # --file
        for target in open(args.file, 'r').readlines():
            target_list.append(target)
    else:
        output.usage()
        sys.exit()

    print('\n[*] starting {0}\n'.format(output.get_time1()))
    output.status_print('检测到 {0} 个目标, 已加载 {1} 条POC'.format(len(target_list), len(poc_modole_list)), 0)
    if run.verify(target_list, poc_modole_list, config.output_path):
        print('\n[+] ending {0}\n'.format(output.get_time1()))
    else:
        output.status_print('程序异常终止', 3)
        sys.exit()
