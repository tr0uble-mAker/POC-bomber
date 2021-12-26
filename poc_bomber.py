#!/usr/bin/env python
#############################
#    Author tr0uble_mAker   #
#############################
# coding=utf-8

from inc import run, init, output, config
import argparse, sys, time

def get_parser():
    parser = argparse.ArgumentParser(usage='python3 pocbomber.py -u http://xxxx -o report.txt',
                                     description='POC Bomber: 基于python3的poc验证框架',
                                     )
    p = parser.add_argument_group('POC-Bomber 的参数')
    p.add_argument("-u", "--url", type=str, help="测试单条url")
    p.add_argument("-f", "--file", type=str, help="测试多个url文件")
    p.add_argument("-o", "--output", help="报告生成路径(默认不生成报告)")
    p.add_argument("--dnslog", type=str, help="使用dnslog平台检测无回显漏洞")
    args = parser.parse_args()
    return args

def get_time():
    return time.strftime("@ %Y-%m-%d /%H:%M:%S/", time.localtime())

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

    print('\n[*] starting {0}\n'.format(get_time()))
    poc_list = init.get_poc_list()
    print('[INFO] 检测到 {0} 个目标, 已加载 {1} 条POC'.format(len(target_list), len(poc_list)))
    if run.run(target_list, poc_list, config.output_path):
        print('\n[+] ending {0}\n'.format(get_time()))
    else:
        print('\n[-] ERROR! 程序异常终止!')
        sys.exit()



if __name__ == '__main__':
    main()
