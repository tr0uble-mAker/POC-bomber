import requests
import re
import urllib


def verify(url):
    relsult = {
        'name': '致远 OA A8 htmlofficeservlet getshell 漏洞',
        'vulnerable': False
    }
    payload = '/seeyon/htmlofficeservlet'
    try:
        vurl = urllib.parse.urljoin(url, payload)
        req = requests.get(vurl, timeout=3)
        if re.search('DBSTEP', req.text) and re.search('htmoffice', req.text):
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['payload'] = vurl
            relsult['about'] = 'http://wyb0.com/posts/2019/seeyon-htmlofficeservlet-getshell/'
        return relsult
    except:
        return relsult


if __name__ == '__main__':
    url = input('url:')
    print(seeyon_oa_a8_htmlofficeservlet_getshell(url))