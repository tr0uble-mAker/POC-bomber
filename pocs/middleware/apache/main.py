from pocs.middleware.apache.CVE_2021_41773 import CVE_2021_41773
from pocs.middleware.apache.CVE_2017_15715 import CVE_2017_15715
from pocs.middleware.apache.log4j2_rce import log4j2_rce

def apache(url):          # 返回poc检测函数字符串列表
    poclist = [
        'log4j2_rce("{0}")'.format(url),
        'CVE_2021_41773("{0}")'.format(url),
        'CVE_2017_15715("{0}")'.format(url),

    ]
    return poclist
