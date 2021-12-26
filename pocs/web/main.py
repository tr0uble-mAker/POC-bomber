#!/usr/bin/env python
# coding=utf-8
from pocs.web.weaver.main import *
from pocs.web.seeyon.main import *
from pocs.web.CVE_2021_22205 import CVE_2021_22205
from pocs.web.ueditor_1433_parsing_vulnerabilitly import ueditor_1433_Parsing_vulnerability
from pocs.web.CVE_2021_21972 import CVE_2021_21972
from pocs.web.CVE_2021_40870 import CVE_2021_40870

def web():
    poclist = []
    poclist = poclist + weaver()
    poclist = poclist + seeyon()
    poclist = poclist + [
        'CVE_2021_22205',
        'CVE_2021_21972',
        'ueditor_1433_Parsing_vulnerability',
        'CVE_2021_40870',
    ]


    return poclist