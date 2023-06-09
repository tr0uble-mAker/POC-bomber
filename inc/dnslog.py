from inc import init
from inc import output, common
import socket, requests
from dnslib import DNSRecord, DNSHeader, RR, A
import time, random, string
import threading
from wsgiref.simple_server import make_server
import base64, json, hashlib

def get_dnslog_domain():
    return ''.join(random.sample(string.digits + string.ascii_letters, 5)) + '.' + common.get_value("dnslog_base_domain")

def start_dnslog_scan():
    thread_dnslogscan = threading.Thread(target=dnslog_scan)
    thread_dnslogscan.start()

def dnslog_add_scan(result):
    if not common.get_value("dnslog_flag"):
        output.put_output_queue(result)
    dnslog_scan_dict = common.get_value("dnslog_scan_dict")
    dnslog_domain = result["dnslog_domain"]
    dnslog_scan_dict[dnslog_domain] = result

def dnslog_scan():
    lock = threading.Lock()
    visted_dict = {}
    while True:
        time.sleep(3)
        if common.get_value("current_times") == common.get_value("total_times"):
            break
        dnslog_rep_json = requests_dnslog_server()
        dnslog_scan_dict = common.get_value("dnslog_scan_dict")
        if len(dnslog_rep_json.keys()) > 0:
            for rep_domain in list(dnslog_rep_json.keys()):
                for dnslog_domain in list(dnslog_scan_dict.keys()):
                    if dnslog_domain.lower() in rep_domain.lower():
                        result = dnslog_scan_dict[dnslog_domain]
                        result["vulnerable"] = True
                        lock.acquire()
                        if visted_dict.get(dnslog_domain):
                            common.set_value("current_times", common.get_value("current_times") - 1)
                        output.put_output_queue(result)
                        lock.release()
                        dnslog_scan_dict.pop(dnslog_domain)
        for dnslog_domain in list(dnslog_scan_dict.keys()):
            if visted_dict.get(dnslog_domain):
                if visted_dict[dnslog_domain] <= 3:
                    visted_dict[dnslog_domain] += 1
                else:
                    visted_dict.pop(dnslog_domain)
                    dnslog_scan_dict.pop(dnslog_domain)
            else:
                result = dnslog_scan_dict[dnslog_domain]
                lock.acquire()
                output.put_output_queue(result)
                lock.release()
                visted_dict[dnslog_domain] = 1


def requests_dnslog_server():
    bs64_str = base64.b64encode(common.get_value("dnslog_auth_token").encode()).decode()
    md5 = hashlib.md5()
    md5.update(bs64_str.encode('utf-8'))
    md5_bs4_token = md5.hexdigest()
    headers = {
        "User-Agent": md5_bs4_token
    }
    timeout = 5
    dnslog_url = f'http://{common.get_value("dnslog_server_ip")}:{common.get_value("dnslog_web_port")}'
    try:
        rep = requests.get(dnslog_url, timeout=timeout, headers=headers)
        return json.loads(rep.text)
    except:
        return {}

def dnslog_server():
    output.log_info("dnslog base domain: " + common.get_value("dnslog_base_domain"))
    dnslog = DnslogServer(
        base_domain=common.get_value("dnslog_base_domain"), is_auth=common.get_value("dnslog_is_auth"),
        auth_token=common.get_value("dnslog_auth_token"), web_port=common.get_value("dnslog_web_port"),
    )
    dnslog.start_dnslog()
    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            output.log_info("user quit!")
            dnslog.close_dnslog()
            break

DNSLOG_INFO_LIST = []

class DnslogServer():
    '''dnslog平台'''
    def __init__(self, base_domain, is_auth, auth_token, web_port):
        self.base_domain = base_domain
        self.is_auth = is_auth
        self.auth_token = auth_token
        self.web_port = web_port
        self.dnsserver = DnsServer(base_domain=self.base_domain)
        self.webserver = WebServer(web_port=self.web_port, is_auth=self.is_auth, auth_token=self.auth_token)

    def start_dnslog(self):
        thread_dnsserver = threading.Thread(target=self.dnsserver.start_dnsServer, args=[])
        thread_webserver = threading.Thread(target=self.webserver.start_webserver, args=[])
        thread_webserver.start()
        thread_dnsserver.start()

    def close_dnslog(self):
        self.dnsserver.close_dnsserver()
        self.webserver.close_webserver()

class DnsServer():
    '''dns服务'''
    def __init__(self, base_domain):
        self.base_domain = base_domain
        self.dns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.query_domain_list = []
        self.close_flag = False

    def start_dnsServer(self):
        self.dns_socket.bind(("", 53))
        output.log_info("start listening dns at port 53 ......")
        while not self.close_flag:
            try:
                data, address = self.dns_socket.recvfrom(1024)
                request = DNSRecord.parse(data)
                qname = request.q.qname
                reply = DNSRecord(
                    DNSHeader(id=request.header.id, qr=1, aa=1, ra=1),
                    q=request.q,
                    a=RR(qname, rdata=A("127.0.0.1"))
                )
                self.dns_socket.sendto(reply.pack(), address)
                self.query_domain_list.append(qname)
                if len(self.base_domain) > 0 and self.base_domain not in str(qname):
                    continue
                DNSLOG_INFO_LIST.append((str(qname), address[0]))
                output.log_success(f"get A query \[{address[0]}]--->\[{qname}]")
            except:
                pass

    def close_dnsserver(self):
        self.close_flag = True
        self.dns_socket.close()

class WebServer():
    '''简易web服务'''
    def __init__(self, web_port, is_auth, auth_token):
        self.web_port = web_port
        self.webserver = make_server("", self.web_port, self.app)
        self.patterns = {
            "/": self.dnslog_web
        }
        self.is_auth = is_auth
        self.auth_token = auth_token

    def error_401(self, start_response):
        start_response("401 not auth", [("Content-Type", "text/plain")])
        return [b"not auth"]

    def error_404(self, start_response):
        start_response("404 not auth", [("Content-Type", "text/plain")])
        return [b"page not found"]

    def dnslog_web(self, *args):
        rep_dict = {}
        for domain, address in DNSLOG_INFO_LIST:
            rep_dict[domain] = address
        return json.dumps(rep_dict)

    def auth(self, auth_str):
        if auth_str == self.encode(self.auth_token):
            return True
        else:
            return False

    def encode(self, str):
        bs64_str = base64.b64encode(str.encode()).decode()
        md5_str = self.md5(bs64_str)
        return md5_str

    def md5(self, str):
        md5 = hashlib.md5()
        md5.update(str.encode('utf-8'))
        md5_str = md5.hexdigest()
        return md5_str

    def app(self, env, start_response):
        url = env.get("PATH_INFO")                  # 获取web端传来的url
        params = env.get("QUERY_STRING")            # 获取web端传入的参数
        auth_token = env.get("HTTP_USER_AGENT")     # 从headers获取auth_token
        if not self.auth(auth_token) and self.is_auth:
            return self.error_401(start_response)
        if (url is None) or (url not in self.patterns.keys()):
            return self.error_404(start_response)
        start_response("200 ok", [("Content-Type", "text/plain")])
        resp = self.patterns.get(url)
        if resp is None:                            # key在路由关系里，但是velue为none的情况处理
            return self.error_404(start_response)
        return [resp(params).encode()]              # 执行视图函数

    def start_webserver(self):
        output.log_info(f"start webserver at port {self.web_port} ......")
        self.webserver.serve_forever()

    def close_webserver(self):
        self.webserver.shutdown()


"""
import requests, os, time
from inc import config
# 支持dnslog平台
class Dnslog():                    # dnslog默认加载配置文件
    def __init__(self):
        self.dnslog_flag = config.dnslog_flag
        self.sessions = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X '
        }
        self.dnslog_timesleep = config.dnslog_timesleep
        self.dnslog_getdomain_url = config.dnslog_getdomain_url
        self.dnslog_getdrep_url = config.dnslog_getrep_url

    def dnslog_getdomain(self):     #获取dnslog随机子域名
        if self.dnslog_flag is not True:
            return False
        try:
            rep = self.sessions.get(self.dnslog_getdomain_url, headers=self.headers, timeout=10, allow_redirects=False, verify=False)
            return rep.text
        except:
            return False

    def dnslog_getrep(self):        # 获取响应
        if self.dnslog_flag is not True:
            return False
        try:
            rep = self.sessions.get(self.dnslog_getdrep_url, headers=self.headers, timeout=10, allow_redirects=False, verify=False)
            return rep.text
        except:
            return False

    def dnslog_sleep(self):       # dnslog休眠
        if self.dnslog_flag is not True:
            return False
        time.sleep(config.dnslog_timesleep)


if __name__ == '__main__':
    dnslog = Dnslog()
    domain = dnslog.dnslog_getdomain()
    os.system('ping {0}'.format('zzz.'+domain))
    print(dnslog.dnslog_getrep())
"""