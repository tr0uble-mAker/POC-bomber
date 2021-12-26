import re
import socket
from time import sleep
from urllib.parse import urlparse
from pocs.middleware.weblogic.CVE_2020_14882 import CVE_2020_14882
from pocs.middleware.weblogic.CVE_2020_2551 import CVE_2020_2551
from pocs.middleware.weblogic.CVE_2019_2890 import CVE_2019_2890
from pocs.middleware.weblogic.CVE_2019_2729 import CVE_2019_2729
from pocs.middleware.weblogic.CVE_2019_2725 import CVE_2019_2725
from pocs.middleware.weblogic.CVE_2018_2894 import CVE_2018_2894
from pocs.middleware.weblogic.CVE_2018_2893 import CVE_2018_2893
from pocs.middleware.weblogic.CVE_2018_2628 import CVE_2018_2628
from pocs.middleware.weblogic.CVE_2017_10271 import CVE_2017_10271
from pocs.middleware.weblogic.CVE_2017_3506 import CVE_2017_3506
from pocs.middleware.weblogic.CVE_2017_3248 import CVE_2017_3248
from pocs.middleware.weblogic.CVE_2016_3510 import CVE_2016_3510
from pocs.middleware.weblogic.CVE_2016_0638 import CVE_2016_0638
from pocs.middleware.weblogic.CVE_2014_4210 import CVE_2014_4210


def weblogic():          # 返回poc检测函数字符串列表
    poclist = [
        'CVE_2020_14882',
        'CVE_2020_2551',
        'CVE_2019_2890',
        'CVE_2019_2729',
        'CVE_2019_2725',
        'CVE_2018_2894',
        'CVE_2018_2893',
        'CVE_2018_2628',
        'CVE_2017_10271',
        'CVE_2017_3506',
        'CVE_2017_3248',
        'CVE_2016_3510',
        'CVE_2016_0638',
        'CVE_2014_4210',

    ]
    return poclist

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
    server_address = (str(host), int(port))
    sock.connect(server_address)
    sock.send(bytes.fromhex('74332031322e322e310a41533a3235350a484c3a31390a4d533a31303030303030300a0a'))
    sleep(1)
    try:
        version = (re.findall(r'HELO:(.*?).false', sock.recv(1024).decode()))[0]
        if version:
            return version
        else:
            return False
    except:
        return False


if __name__ == '__main__':
    url = input('url:')
    print(weblogic_fingerprint(url))
