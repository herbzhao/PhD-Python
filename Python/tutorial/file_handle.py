# -*- coding: utf-8 -*-
#file manipulation 
"""
Created on Mon Oct 24 22:09:43 2016

@author: herbz
"""



f = open('random.txt','r+')
f.write('today111111')
f.seek(0)
f_read = f.read()
print(f_read)

import pprint
cats = [{'name': 'Zophie', 'desc': 'chubby'}, {'name': 'Pooka', 'desc': 'fluffy'}]

cats = pprint.pformat(cats)
f = open('py_storage.py','a+')
f.write('kitty = ' + cats + '\n')
f.close()

000
import py_storage
py_storage.kitty
py_storage.kitty[0]
