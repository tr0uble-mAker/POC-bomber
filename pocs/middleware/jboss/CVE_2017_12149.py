import requests
import urllib
import re

def verify(url):
    relsult = {
        'name': 'Jboss反序列化漏洞 (CVE-2017-12149)',
        'vulnerable': False
    }
    try:
        payload = '/invoker/readonly'
        vurl = urllib.parse.urljoin(url, payload)
        req = requests.get(vurl, timeout=3)
        if req.status_code == 500 and re.search('jboss', req.text):
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['method'] = 'GET'
            relsult['payload'] = vurl
            relsult['about'] = 'https://github.com/yunxu1/jboss-_CVE-2017-12149'
        return relsult
    except:
        return relsult


if __name__ == '__main__':
    url = input('url:')
    print(CVE_2017_12149(url))