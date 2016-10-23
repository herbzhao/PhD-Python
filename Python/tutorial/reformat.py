# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 21:14:53 2016

@author: herbz
"""

#! python3
# bulletPointAdder.py - Adds Wikipedia bullet points to the start
# of each line of text on the clipboard.


raw_file = 'Lists of animals\nLists of aquarium life\nLists of biologists by author abbreviation\nLists of cultivars'

print(raw_file)

# TODO: Separate lines and add stars.
lines = raw_file.split('\n')
print(lines)

new_file = ''

for i in range(len(lines)):
    print(r'*'+lines[i])
    new_file = new_file + '*' + lines[i] + '\n'

print(new_file)