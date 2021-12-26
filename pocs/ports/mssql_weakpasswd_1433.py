import pymssql
import re, socket
from urllib.parse import urlparse
from inc import config

def is_ip(url):
    if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", url):
        return True
    else:
        return False

def is_open(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(1)
        s.connect((host, int(port)))
        s.shutdown(2)
        return True
    except:
        return False

def mssql_weakpasswd_1443(url):
    relsult = {
        'name': 'Mssql(port=1433)弱口令',
        'vulnerable': False
    }
    mssql_username = ('sa', 'admin', 'mssql')
    mssql_weak_password = ('', '123456', 'test', 'root', 'admin', 'user')  # 密码字典
    oH = urlparse(url)
    a = oH.netloc.split(':')
    port = 1433         # mssql默认端口
    host = a[0]        #数据库IP地址
    if is_ip(host) is not True or is_open(host, port) is False:  # 不是ip或端口未开放直接退出
        return relsult
    for username in mssql_username:
        for password in mssql_weak_password:
            try:
                print('[+]',username, ':', password)
                db = pymssql.connect(server=host, port=port, user=username, password=password, timeout=1)
                relsult['vulnerable'] = True
                relsult['host'] = host
                relsult['port'] = port
                relsult['username'] = username
                relsult['password'] = password
                return relsult
            except:
                pass
    return relsult

if __name__ == '__main__':
    host = input('host:')
    print(mssql_weakpasswd_1443(host))