from pocs.middleware.apache.CVE_2021_41773 import CVE_2021_41773
from pocs.middleware.apache.CVE_2017_15715 import CVE_2017_15715
from pocs.middleware.apache.log4j2_rce import log4j2_rce
from pocs.middleware.apache.CVE_2021_42013 import CVE_2021_42013

def apache():          # 返回poc检测函数字符串列表
    poclist = [
        'log4j2_rce',
        'CVE_2021_41773',
        'CVE_2017_15715',
        'CVE_2021_42013'

    ]
    return poclist
