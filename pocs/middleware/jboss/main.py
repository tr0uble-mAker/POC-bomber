from pocs.middleware.jboss.CVE_2017_12149 import CVE_2017_12149
from pocs.middleware.jboss.CVE_2017_7504 import CVE_2017_7504
from pocs.middleware.jboss.CVE_2017_7501 import CVE_2017_7501

def jboss(url):          # 返回poc检测函数字符串列表
    poclist = [
        'CVE_2017_12149("{0}")'.format(url),
        'CVE_2017_7504("{0}")'.format(url),
        'CVE_2017_7504("{0}")'.format(url),


    ]
    return poclist