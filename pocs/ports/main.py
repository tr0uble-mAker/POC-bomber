from pocs.ports.redis_6379 import redis_6379
from pocs.ports.mssql_weakpasswd_1433 import mssql_weakpasswd_1443

def ports():          # 返回poc检测函数字符串列表
    poclist = [
        'redis_6379',

    ]
    return poclist