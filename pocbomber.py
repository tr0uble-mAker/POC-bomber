#!/usr/bin/env python
# coding=utf-8
  ############################
 #   Author tr0uble_mAker   #
###########################

from inc import run, init, output, config
from inc import console
import argparse, sys, time

def get_parser():
    parser = argparse.ArgumentParser(usage='python3 pocbomber.py -u http://xxxx -o report.txt',
                                     description='POC bomber: 基于python3的poc/exp集成框架',
                                     )
    p = parser.add_argument_group('POC-Bomber 的参数')
    p.add_argument("-u", "--url", type=str, help="测试单条url")
    p.add_argument("-f", "--file", type=str, help="测试多个url文件")
    p.add_argument("-o", "--output", type=str, help="报告生成路径(默认不生成报告)")
    p.add_argument("-p", "--poc", type=str, help='指定单个或多个poc进行检测, 直接传入poc文件名, 多个poc用(,)分开')
    p.add_argument("-t", "--thread", type=int, help="指定线程池最大并发数量")
    p.add_argument("--show", action='store_true', help="列所有出poc/exp的详细信息")
    p.add_argument("--attack", action='store_true', help="使用poc文件中的exp进行攻击")
    p.add_argument("--dnslog", action='store_true', help="使用dnslog平台检测无回显漏洞")
    args = parser.parse_args()
    return args


def main():
    output.logo()
    args = get_parser()
    console.pocbomber_console(args)


if __name__ == '__main__':
    main()



