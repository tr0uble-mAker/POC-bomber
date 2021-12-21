# POC bomber 配置文件


# 指定输出结果路径(为空则默认不生成结果)
report_path = r'漏洞报告.txt'

# 单url测试默认线程(建议线程 < 5)
thread_num_single = 3

# 线程超时时间
thread_timeout = 15


## Dnslog 配置(用于检测无回显rce)
# dnslog获取域名(默认使用 dnslog.cn 检测)
dnslog_getdomain_url = 'http://www.dnslog.cn/getdomain.php'
# dnslog获取响应
dnslog_getrep_url = 'http://www.dnslog.cn/getrecords.php'

# ceye配置(如果使用ceye将ceye参数置为True, 并配置域名和api)
ceye = False
# 配置ceye域名
ceye_domain = ''
# 配置api参数
ceye_api = ''
