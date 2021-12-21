import requests, os, time
from inc import config

# 支持dnslog平台和ceye平台(要使用ceye平台在 /inc/config.py 配置api等参数)
class Dnslog():                    # dnslog默认加载配置文件
    def __init__(self):
        self.sessions = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X '
        }
        self.dnslog_timesleep = config.dnslog_timesleep
        self.dnslog_getdomain_url = config.dnslog_getdomain_url
        self.dnslog_getdrep_url = config.dnslog_getrep_url
        self.ceye = config.ceye
        self.ceye_domain =config.ceye_domain
        self.ceye_api = config.ceye_api

    def dnslog_getdomain(self):     #获取dnslog随机子域名
        try:
            if self.ceye:
                return self.ceye_domain
            else:
                rep = self.sessions.get(self.dnslog_getdomain_url, headers=self.headers, timeout=10, allow_redirects=False, verify=False)
                return rep.text
        except:
            return False

    def dnslog_getrep(self):        # 获取响应
        try:
            if self.ceye:
                ceye_getrep_url = 'http://api.ceye.io/v1/records?token={0}&type=dns'.format(self.ceye_api)
                rep = self.sessions.get(ceye_getrep_url, headers=self.headers, timeout=10, allow_redirects=False, verify=False)
                return rep.text
            else:
                rep = self.sessions.get(self.dnslog_getdrep_url, headers=self.headers, timeout=10, allow_redirects=False, verify=False)
                return rep.text
        except:
            return False


    def dnslog_sleep(self):       # dnslog休眠
        time.sleep(config.dnslog_timesleep)


if __name__ == '__main__':
    dnslog = Dnslog()
    domain = dnslog.dnslog_getdomain()
    os.system('ping {0}'.format('zzz.'+domain))
    print(dnslog.dnslog_getrep())
