import socket
from urllib.parse import urlparse

def verify(url):
    relsult = {
        'name': 'Memcahe 未授权访问',
        'url': url,
        'port': 11211,
        'vulnerable': False,
        'attack': False,
        'about': 'https://blog.csdn.net/chest_/article/details/105808673, https://blog.csdn.net/qq_23936389/article/details/81256118',
    }
    timeout = 3
    oH = urlparse(url)
    a = oH.netloc.split(':')
    port = relsult['port']        # memcache默认端口
    host = a[0]
    if is_open(host, port):
        pass
    else:
        return relsult
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
            return relsult
    except:
        return relsult

def is_open(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(1.5)
        s.connect((host, int(port)))
        s.shutdown(2)
        return True
    except:
        return False