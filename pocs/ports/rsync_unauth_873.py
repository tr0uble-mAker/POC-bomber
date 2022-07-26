import socket
import re
from urllib.parse import urlparse


def verify(url):
    relsult = {
        'name': 'Rsync 未授权访问',
        'vulnerable': False
    }
    timeout = 3
    oH = urlparse(url)
    a = oH.netloc.split(':')
    port = 873        # rsync默认端口873
    host = a[0]
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
            relsult['url'] = url
            relsult['port'] = port
            relsult['about'] = 'https://www.freebuf.com/articles/web/317695.html'
            return relsult
    except:
        return relsult
