#!/usr/bin/env python
# coding=utf-8

from inc import run, output, config

def main():
    output.logo()
    choice = input(" 是否进行单URL检测(Y/n)?")
    if choice == 'n':
        path = input('\n 输入目标路径 >')
        thread_num = input('\n 输入线程数量(建议线程数量20-30) >')
        file = open(path, 'r')
        for url in file.readlines():
            url = url.replace('\n', '')
            report = run.run(url, int(thread_num))
            output.output(report, config.report_path)
        file.close()
    else:
        url = input('\n 输入目标URL >')
        report = run.run(url, config.thread_num_single)
        output.output(report, config.report_path)


if __name__ == '__main__':
    main()



