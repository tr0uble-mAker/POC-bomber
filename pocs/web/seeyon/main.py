from pocs.web.seeyon.seeyon_oa_a8_htmlofficeservlet_getshell import seeyon_oa_a8_htmlofficeservlet_getshell
from pocs.web.seeyon.seeyon_get_sessionslist import sessyon_get_sessionslist
from pocs.web.seeyon.seeyon_a6_sqli import sessyon_a6_sqli


def seeyon(url):          # 致远 漏洞检测模块
    poclist = [
        'seeyon_oa_a8_htmlofficeservlet_getshell("{0}")'.format(url),
        'sessyon_get_sessionslist("{0}")'.format(url),
        'sessyon_a6_sqli("{0}")'.format(url),
    ]
    return poclist