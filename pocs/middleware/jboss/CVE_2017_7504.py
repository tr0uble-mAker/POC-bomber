import requests
import urllib
import re

def verify(url):
    relsult = {
        'name': 'Jboss反序列化漏洞 (CVE-2017-7504)',
        'vulnerable': False
    }
    try:
        payload = '/jbossmq-httpil/HTTPServerILServlet'
        vurl = urllib.parse.urljoin(url, payload)
        req = requests.get(vurl, timeout=3)
        if req.status_code == 200 and re.search('This is the JBossMQ HTTP-IL', req.text):
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['method'] = 'GET'
            relsult['payload'] = vurl
            relsult['about'] = 'https://github.com/ggyao/jbossscan, https://github.com/joaomatosf/JavaDeserH2HC'
        return relsult
    except:
        return relsult

