from pocs.middleware.jboss.CVE_2017_12149 import CVE_2017_12149
from pocs.middleware.jboss.CVE_2017_7504 import CVE_2017_7504
from pocs.middleware.jboss.CVE_2017_7501 import CVE_2017_7501

def jboss():          # 返回poc检测函数字符串列表
    poclist = [
        'CVE_2017_12149',
        'CVE_2017_7504',
        'CVE_2017_7504',


    ]
    return poclist