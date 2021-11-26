#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import socket,argparse,sys
from urllib.parse import urlparse

"""
only check CVE-2020-2551 vuls
Twitter: @Hktalent3135773
Creator: 51pwn_com
Site: https://51pwn.com
How use:
python3 CVE-2020-2551.py -u http://192.168.26.79:7001
# 32 Thread check
cat allXXurl.txt|grep -Eo 'http[s]?:\/\/[^ \/]+'|sort -u|python3 CVE-2020-2551.py -e
"""

def doSendOne(ip,port,data):
    sock=None
    res=None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(7)
        server_addr = (ip, int(port))
        sock.connect(server_addr)
        sock.send(data)
        res = sock.recv(20)
        if b'GIOP' in res:
            return True
    except Exception as e:
        pass
    finally:
        if sock!=None:
            sock.close()
    return False

def doOne(url):
    oH=urlparse(url)
    a=oH.netloc.split(':')
    port=80
    if 2 == len(a):
        port=a[1]
    elif 'https' in oH.scheme:
        port=443
    if doSendOne(a[0],port,bytes.fromhex('47494f50010200030000001700000002000000000000000b4e616d6553657276696365')):
        return True
    else:
        return False
def CVE_2020_2551(url):
    relsult = {
        'name': 'CVE_2020_2551(weblogic)',
        'vulnerable': False
    }
    try:
        if doOne(url):
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['about'] = 'https://github.com/rockmelodies/CVE-2020-2551'
        return relsult
    except:
        return relsult


if __name__=='__main__':
    file = open(r'mrb.txt', 'r')
    for url in file.readlines():
        print('[+] testing:', url)
        if doOne(url):
            print('[@] ok:', url)
            vulurl = open('vulurl.txt', 'a+')
            vulurl.write(url)
            vulurl.write('\n')
    file.close()
