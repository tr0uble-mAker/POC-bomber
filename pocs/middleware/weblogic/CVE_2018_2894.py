#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import sys
import requests
from urllib.parse import urlparse

VUL=['CVE-2018-2894']


def islive(ur,port):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    url='http://' + str(ur)+':'+str(port)+'/ws_utc/begin.do'
    r1 = requests.get(url, headers=headers, timeout=10)
    url='http://' + str(ur)+':'+str(port)+'/ws_utc/config.do'
    r2 = requests.get(url, headers=headers, timeout=10)
    return r1.status_code,r2.status_code

def run(rip,rport):
    a,b=islive(rip,rport)
    if a == 200 or b == 200:
        return True
    else:
        return False
def CVE_2018_2894(url):
    relsult = {
        'name': 'CVE_2018_2894(weblogic)',
        'vulnerable': False
    }
    try:
        oH = urlparse(url)
        a = oH.netloc.split(':')
        port = 80
        if 2 == len(a):
            port = a[1]
        elif 'https' in oH.scheme:
            port = 443
        host = a[0]
        if run(host, port):
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['about'] = 'https://github.com/rabbitmask/WeblogicScan/blob/master/poc/CVE_2018_2894.py'
        return relsult
    except:
        return relsult
if __name__=="__main__":
    url = input('输入目标URL:')
    print(CVE_2018_2894(url))
