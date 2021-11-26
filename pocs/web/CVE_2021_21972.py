import random
import requests
import http.client
import urllib3,urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

TARGET_URI = "/ui/vropspluginui/rest/services/uploadova"

def get_ua():
    first_num = random.randint(55, 62)
    third_num = random.randint(0, 3200)
    fourth_num = random.randint(0, 140)
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_12_6)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                  )
    return ua

def CVE_2021_21972(url):
    relsult = {
        'name': 'CVE-2021-21972 vSphere Client RCE',
        'vulnerable': False
    }
    proxies = {"scoks5": "http://127.0.0.1:1081"}
    headers = {
        'User-Agent': get_ua(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = '/ui/vropspluginui/rest/services/uploadova'
    targetUrl = urllib.parse.urljoin(url, payload)
    try:
        res = requests.get(targetUrl,
                            headers=headers,
                            timeout=10,
                            verify=False,
                            proxies=proxies)
                            # proxies={'socks5': 'http://127.0.0.1:1081'})
        # print(len(res.text))
        if res.status_code == 405:
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['about'] = 'https://github.com/QmF0c3UK/CVE-2021-21972-vCenter-6.5-7.0-RCE-POC/blob/main/CVE-2021-21972.py,https://github.com/0xAgun/CVE-2021-40870/blob/main/poc.py'
            # print("[+] Command success result: " + res.text + "\n")
            return relsult
        else:
            return relsult
    # except Exception as e:
    #     print(e)
    except:
        return relsult



if __name__ == "__main__":
    print(CVE_2021_21972('https://202.178.122.132'))