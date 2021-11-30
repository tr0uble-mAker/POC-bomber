import requests
import urllib
import re

def CVE_2017_7501(url):
    relsult = {
        'name': 'Jboss反序列化漏洞 (CVE-2017-7501)',
        'vulnerable': False
    }
    try:
        payload = '/invoker/JMXInvokerServlet'
        vurl = urllib.parse.urljoin(url, payload)
        req = requests.get(vurl, timeout=3)
        if req.status_code == 200 and re.search(r'jboss', req.text) and re.search(r'java', req.text):
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['method'] = 'GET'
            relsult['payload'] = vurl
            relsult['about'] = 'https://github.com/ggyao/jbossscan, https://github.com/joaomatosf/JavaDeserH2HC'
        return relsult
    except:
        return relsult


if __name__ == '__main__':
    url = input('url:')
    print(CVE_2017_7501(url))