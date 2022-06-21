import requests
import urllib, re

def verify(url):
    relsult = {
        'name': 'jolokia Realm JNDI RCE',
        'vulnerable': False,
        'attack': False,
        'url': url,
        'about': 'https://github.com/LandGrey/SpringBootVulExploit#0x05jolokia-realm-jndi-rce',
    }

    try:
        vurl = urllib.parse.urljoin(url, '/jolokia/list')
        rep = requests.get(vurl, verify=False, timeout=5)
        if rep.status_code == 200 and re.search('type=MBeanFactory', rep.text) and re.search('createJNDIRealm', rep.text):
            relsult['vulnerable'] = True
            return relsult
        else:
            return relsult
    except:
        return relsult