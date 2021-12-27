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
