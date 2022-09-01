import requests
import urllib, re

def verify(url):
    relsult = {
        'name': 'CVE-2021-21972 vSphere Client RCE',
        'vulnerable': False,
        'url': url,
        'about': 'https://github.com/QmF0c3UK/CVE-2021-21972-vCenter-6.5-7.0-RCE-POC/blob/main/CVE-2021-21972.py, https://github.com/0xAgun/CVE-2021-40870/blob/main/poc.py'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
        "Content-Type": "application/x-www-form-urlencoded"
    }
    version_path = '/sdk/vimServiceVersions.xml'
    payload = '/ui/vropspluginui/rest/services/uploadova'
    timeout = 3
    vurl = urllib.parse.urljoin(url, payload)
    finger_url = urllib.parse.urljoin(url, version_path)
    try:
        finger_rep = requests.get(finger_url, headers=headers, timeout=timeout, verify=False)
        if re.search("<version>.+</version>", finger_rep.text):
            rep = requests.get(vurl, headers=headers, timeout=timeout, verify=False)
            if rep.status_code == 405 and 'Method Not Allowed' in rep.text:
                relsult['vulnerable'] = True
        return relsult
    except:
        return relsult



