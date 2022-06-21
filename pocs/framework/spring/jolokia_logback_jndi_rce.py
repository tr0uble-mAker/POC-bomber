import requests
import urllib, re

def verify(url):
    relsult = {
        'name': 'jolokia logback JNDI RCE',
        'vulnerable': False,
        'attack': False,
        'url': url,
        'about': 'https://github.com/LandGrey/SpringBootVulExploit#0x04jolokia-logback-jndi-rce',
    }

    try:
        vurl = urllib.parse.urljoin(url, '/jolokia/list')
        rep = requests.get(vurl, verify=False, timeout=5)
        if rep.status_code == 200 and re.search('ch\.qos\.logback\.classic\.jmx\.JMXConfigurator', rep.text) and re.search('reloadByURL', rep.text):
            relsult['vulnerable'] = True
            return relsult
        else:
            return relsult
    except:
        return relsult


