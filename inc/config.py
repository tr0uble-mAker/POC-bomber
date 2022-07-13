# POC bomber 配置文件

# 输出文件(默认为空)
output_path = r''

# 线程池最大数量
max_thread = 300


## Dnslog 配置(用于检测无回显rce)
# 使用dnslog开启此开关
dnslog_flag = False
# dnslog 默认等待时间
dnslog_timesleep = 6
# 获取随机域名(默认使用 dnslog.cn 检测)
dnslog_getdomain_url = 'http://www.dnslog.cn/getdomain.php'
# 获取 dnslog 记录响应
dnslog_getrep_url = 'http://www.dnslog.cn/getrecords.php'


