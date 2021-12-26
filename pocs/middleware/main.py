#!/usr/bin/env python
# coding=utf-8

from pocs.middleware.apache.main import *
from pocs.middleware.weblogic.main import *
from pocs.middleware.jboss.main import *


def middleware():
    poclist = []
    poclist = poclist + weblogic()
    poclist = poclist + apache()
    poclist = poclist + jboss()


    return poclist