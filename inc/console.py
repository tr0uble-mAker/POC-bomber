#!/usr/bin/env python
# coding=utf-8

from inc import run, init, output, config
import argparse, sys, time

# POC bomber 控制台        参数处理和程序调用
def pocbomber_console(args):
    attack = False
    poc_modole_list = init.get_poc_modole_list()
    target_list = []
    if args.output:                             # --output
        config.output_path = args.output
    if args.thread:                             # --thread
        config.max_thread = args.thread
    if args.dnslog:                             # --dnslog
        config.dnslog_flag = True
    if args.poc:                                # --poc
        poc_modole_list = init.get_poc_modole_list_by_search(args.poc.split(','))
    if args.show:
        output.show(poc_modole_list)
        sys.exit()
    if args.attack:
        attack = True
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
        if attack:
            output.status_print('检测到--attack参数, 开始尝试调用exp', 0)
            if run.attack(target_list[0], poc_modole_list[0]):
                output.status_print('ATTACK END! enjoy : ) ', 1)
            else:
                output.status_print('ATTACK FAIL! What\'s wrong?', 3)
    else:
        output.status_print('程序异常终止', 3)
        sys.exit()
    print('\n[+] ending {0}\n'.format(output.get_time1()))



