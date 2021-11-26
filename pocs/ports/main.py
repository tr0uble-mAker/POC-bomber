from pocs.ports.redis_6379 import redis_6379

def ports(url):          # 返回poc检测函数字符串列表
    print('\n[+] 正在加载 常见端口漏洞,弱口令爆破 poc检测模块......')
    poclist = [
        'redis_6379("{0}")'.format(url),

    ]
    return poclist