import socket
from urllib.parse import urlparse

def verify(url):
    relsult = {
        'name': 'Memcahe 未授权访问',
        'url': url,
        'vulnerable': False,
        'attack': False,
        'about': 'https://blog.csdn.net/chest_/article/details/105808673, https://blog.csdn.net/qq_23936389/article/details/81256118',
    }
    timeout = 3
    oH = urlparse(url)
    a = oH.netloc.split(':')
    port = 11211        # memcache默认端口11211
    host = a[0]
    payload = b'stats\r\n'  # 发送的数据
    s = socket.socket()
    socket.setdefaulttimeout(timeout)  # 设置超时时间
    try:
        s.connect((host, int(port)))
        s.send(payload)  # 发送info命令
        response = s.recv(1024).decode()
        s.close()
        if response and 'STAT version' in response:
            relsult['vulnerable'] = True
            relsult['port'] = port
            return relsult
    except:
        return relsult