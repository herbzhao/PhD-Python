# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 22:43:17 2016

@author: herbz
"""

import re

email = 'HERBZHAO@gmail.cn'

string = r'@(\w)\w*'

email_re = re.compile(r'@(\w)\w*',re.VERBOSE)    #@(g)mail
result = email_re.search('herbzhao@gmail.com')
result = email_re.sub(r'@\1***',r'herbzhao@gmail.com')

#result.group()
