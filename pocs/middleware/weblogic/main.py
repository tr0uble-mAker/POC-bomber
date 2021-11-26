from pocs.middleware.weblogic.CVE_2020_2551 import CVE_2020_2551
from pocs.middleware.weblogic.CVE_2019_2890 import CVE_2019_2890
from pocs.middleware.weblogic.CVE_2019_2729 import CVE_2019_2729
from pocs.middleware.weblogic.CVE_2019_2725 import CVE_2019_2725
from pocs.middleware.weblogic.CVE_2018_2894 import CVE_2018_2894
from pocs.middleware.weblogic.CVE_2018_2893 import CVE_2018_2893
from pocs.middleware.weblogic.CVE_2018_2628 import CVE_2018_2628
from pocs.middleware.weblogic.CVE_2017_10271 import CVE_2017_10271
from pocs.middleware.weblogic.CVE_2017_3506 import CVE_2017_3506
from pocs.middleware.weblogic.CVE_2017_3248 import CVE_2017_3248
from pocs.middleware.weblogic.CVE_2016_3510 import CVE_2016_3510
from pocs.middleware.weblogic.CVE_2016_0638 import CVE_2016_0638
from pocs.middleware.weblogic.CVE_2014_4210 import CVE_2014_4210
def weblogic(url):          # 返回poc检测函数字符串列表
    poclist = [
        #'CVE_2020_2551("{0}")'.format(url),
        'CVE_2019_2890("{0}")'.format(url),
        'CVE_2019_2729("{0}")'.format(url),
        'CVE_2019_2725("{0}")'.format(url),
        'CVE_2018_2894("{0}")'.format(url),
        'CVE_2018_2893("{0}")'.format(url),
        'CVE_2018_2628("{0}")'.format(url),
        'CVE_2017_10271("{0}")'.format(url),
        'CVE_2017_3506("{0}")'.format(url),
        'CVE_2017_3248("{0}")'.format(url),
        'CVE_2016_3510("{0}")'.format(url),
        'CVE_2016_0638("{0}")'.format(url),
        'CVE_2014_4210("{0}")'.format(url),

    ]
    return poclist

