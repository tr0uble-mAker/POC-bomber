# POC bomber config

# 进度显示(默认开启)
show_progress = True
# 输出文件(默认为空)
output_path = r''

# 线程池最大数量
max_threads = 30
# 单条poc最大超时
timeout = 15
# 休眠间隔(默认不休眠，如开启线程默认1)
delay = 0


## Dnslog 配置(需要在vps上启动poc-bomber的dnslog服务端)
# 自己购买域名设置的ns记录(对应a记录指向vps)
dnslog_base_domain = ""
# dnslog是否需要认证
dnslog_is_auth = True
# 如需认证,在此配置密码
dnslog_auth_token = "123456"
# dnslog http服务端口
dnslog_web_port = 5000
# dnslog服务端ip
dnslog_server_ip = ""



