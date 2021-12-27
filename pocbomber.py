#!/usr/bin/env python
# coding=utf-8

from inc import run, init, output, config
import argparse, sys, time

def get_parser():
    parser = argparse.ArgumentParser(usage='python3 pocbomber.py -u http://xxxx -o report.txt',
                                     description='POC bomber: 基于python3的poc/exp集成框架',
                                     )
    p = parser.add_argument_group('POC-Bomber 的参数')
    p.add_argument("-u", "--url", type=str, help="测试单条url")
    p.add_argument("-f", "--file", type=str, help="测试多个url文件")
    p.add_argument("-o", "--output", type=str, help="报告生成路径(默认不生成报告)")
    p.add_argument("--dnslog", action='store_true', help="使用dnslog平台检测无回显漏洞")
    args = parser.parse_args()
    return args


def main():
    output.logo()
    args = get_parser()
    target_list = []
    if args.output:
        config.output_path = args.output
    if args.dnslog:
        config.dnslog_flag = True
    if args.url and args.file is None:
        target_list.append(args.url)
    elif args.file and args.url is None:
        for target in open(args.file, 'r').readlines():
            target_list.append(target)
    else:
        output.usage()
        sys.exit()

    print('\n[*] starting {0}\n'.format(output.get_time1()))
    poc_modole_list = init.get_poc_modole_list()
    output.status_print('检测到 {0} 个目标, 已加载 {1} 条POC'.format(len(target_list), len(poc_modole_list)), 0)
    if run.verify(target_list, poc_modole_list, config.output_path):
        print('\n[+] ending {0}\n'.format(output.get_time1()))
    else:
        output.status_print('程序异常终止', 3)
        sys.exit()



if __name__ == '__main__':
    main()



