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

def struct2(url):
    poclist = [
        's2_052("{0}")'.format(url),
        's2_061("{0}")'.format(url),
        's2_001("{0}")'.format(url),
        's2_005("{0}")'.format(url),
        's2_007("{0}")'.format(url),
        's2_008("{0}")'.format(url),
        's2_009("{0}")'.format(url),
        's2_012("{0}")'.format(url),
        's2_013("{0}")'.format(url),
        's2_015("{0}")'.format(url),
        's2_016("{0}")'.format(url),
        's2_032("{0}")'.format(url),
        's2_045("{0}")'.format(url),
        's2_046("{0}")'.format(url),
        's2_048("{0}")'.format(url),
        's2_053("{0}")'.format(url),
        's2_057("{0}")'.format(url),
    ]
    return poclist
