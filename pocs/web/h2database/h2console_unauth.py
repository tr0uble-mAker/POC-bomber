import requests
import re
import urllib

def verify(url):
    relsult = {
        'name': 'H2-Database-Console 未授权访问',
        'vulnerable': False,
        'attack': False,
        'about': 'https://blog.csdn.net/weixin_45366453/article/details/125525496, https://blog.csdn.net/zy15667076526/article/details/111413979'
    }
    timeout = 3
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    }
    vurl = urllib.parse.urljoin(url, '/h2-console/login.jsp')
    try:
        rep = requests.get(vurl, headers=headers, verify=False, timeout=timeout)
        if rep.status_code == 200 and re.search('Welcome to H2', rep.text) and re.search('H2 Console', rep.text):
            relsult['vulnerable'] = True
            relsult['vurl'] = vurl
        return relsult
    except:
        return relsult
