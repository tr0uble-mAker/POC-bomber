import socket
from urllib.parse import urlparse

def verify(url):
    relsult = {
        'name': 'Zookeeper未授权访问',
        'url': url,
        'vulnerable': False,
        'attack': False,
        'about': 'https://www.cnblogs.com/stuka/p/14716926.html',
    }
    timeout = 3
    oH = urlparse(url)
    host = oH.netloc.split(':')[0]
    port1 = 2181
    port2 = 2182
    if is_open(host, port1) or is_open(host, port2):
        pass
    else:
        return relsult
    try:
        if check(host, port1, timeout):
            relsult['vulnerable'] = True
            relsult['port'] = port1
        if check(host, port2, timeout):
            relsult['vulnerable'] = True
            relsult['port'] = port2
        return relsult
    except:
        return relsult


def check(ip, port, timeout):
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        flag = b'envi'
        s.send(flag)
        data = s.recv(1024)
        s.close()
        if 'Environment' in str(data):
            return True
    except:
        return False

def is_open(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(1.5)
        s.connect((host, int(port)))
        s.shutdown(2)
        return True
    except:
        return False