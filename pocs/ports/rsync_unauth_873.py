import socket
import re
from urllib.parse import urlparse

def is_open(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(1.5)
        s.connect((host, int(port)))
        s.shutdown(2)
        return True
    except:
        return False

def verify(url):
    relsult = {
        'name': 'Rsync 未授权访问',
        'vulnerable': False,
        'url': url,
        'port': 873,
        'about': 'https://www.freebuf.com/articles/web/317695.html',
    }
    timeout = 3
    oH = urlparse(url)
    a = oH.netloc.split(':')
    port = relsult['port']        # rsync默认端口
    host = a[0]
    if is_open(host, port):
        pass
    else:
        return relsult
    payload = b''  # 发送的数据
    s = socket.socket()
    socket.setdefaulttimeout(timeout)  # 设置超时时间
    try:
        s.connect((host, int(port)))
        s.send(payload)  # 发送info命令
        response = s.recv(1024).decode()
        s.close()
        if response and '@RSYNCD' in response:
            relsult['vulnerable'] = True
            return relsult
    except:
        return relsult
