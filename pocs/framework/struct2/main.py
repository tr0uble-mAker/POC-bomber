#!/usr/bin/env python
# coding=utf-8
from pocs.framework.struct2.s2_001 import s2_001
from pocs.framework.struct2.s2_005 import s2_005
from pocs.framework.struct2.s2_007 import s2_007
from pocs.framework.struct2.s2_008 import s2_008
from pocs.framework.struct2.s2_009 import s2_009
from pocs.framework.struct2.s2_012 import s2_012
from pocs.framework.struct2.s2_013 import s2_013
from pocs.framework.struct2.s2_015 import s2_015
from pocs.framework.struct2.s2_016 import s2_016
from pocs.framework.struct2.s2_032 import s2_032
from pocs.framework.struct2.s2_045 import s2_045
from pocs.framework.struct2.s2_046 import s2_046
from pocs.framework.struct2.s2_048 import s2_048
from pocs.framework.struct2.s2_052 import s2_052
from pocs.framework.struct2.s2_053 import s2_053
from pocs.framework.struct2.s2_057 import s2_057
from pocs.framework.struct2.s2_061 import s2_061

def struct2():
    poclist = [
        's2_057',
        # 's2_052',
        's2_061',
        's2_001',
        's2_005',
        's2_007',
        's2_008',
        's2_009',
        's2_012',
        's2_013',
        's2_015',
        's2_016',
        's2_032',
        's2_045',
        's2_046',
        's2_048',
        's2_053',
    ]
    return poclist

if __name__ == '__main__':
    url = input('struct2全版本检测,输入url:')
    report = []
    for poc in struct2():
        relsult = eval(poc + '("{0}")'.format(url))
        if relsult['vulnerable']:
            report.append(relsult)
    for r in report:
        print(r)