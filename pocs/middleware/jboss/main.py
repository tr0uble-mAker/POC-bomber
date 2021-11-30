from pocs.middleware.jboss.CVE_2017_12149 import CVE_2017_12149

def jboss(url):          # 返回poc检测函数字符串列表
    poclist = [
        'CVE_2017_12149("{0}")'.format(url),

    ]
    return poclist