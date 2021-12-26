from pocs.web.weaver.CNVD_2021_49104 import CNVD_2021_49104
from pocs.web.weaver.e_cology_v8_sqli import e_cology_v8_sqli
from pocs.web.weaver.CNVD_2019_32204 import CNVD_2019_32204
from pocs.web.weaver.CNVD_2019_34241 import CNVD_2019_34241
from pocs.web.weaver.e_cology_workflowservicexml_rce import e_cology_workflowservicexml_rce
from pocs.web.weaver.weaver_common_ctrl_upload import weaver_common_ctrl_upload

def weaver():          # 泛微 漏洞检测模块
    poclist = [
        'CNVD_2021_49104',
        'e_cology_v8_sqli',
        'CNVD_2019_32204',
        'CNVD_2019_34241',
        'e_cology_workflowservicexml_rce',
        'weaver_common_ctrl_upload',


    ]
    return poclist