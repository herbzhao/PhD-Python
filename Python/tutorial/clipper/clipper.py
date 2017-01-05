# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


#multiclipboard
# mcb.pyw - Saves and loads pieces of text to the clipboard.

# Usage: py.exe mcb.pyw save <keyword> - Saves clipboard to keyword.
   #py.exe mcb.pyw <keyword> - Loads keyword to clipboard.
   #py.exe mcb.pyw list - Loads all keywords to clipboard.

import shelve, pyperclip, sys

#create a new shelf binary file
mcbShelf = shelve.open('mcb')

print(sys.argv)
# TODO: Save clipboard content.
if len(sys.argv) > 1:
    if sys.argv[1].lower() == 'save':
        mcbShelf[sys.argv[2]] = pyperclip.paste()

    elif sys.argv[1].lower() == 'list':
        pyperclip.copy(str(list(mcbShelf.keys())))
        print(list(mcbShelf.keys()))
        #convert keys to string for copy purpose
    elif sys.argv[1].lower() == 'delete':
        if len(sys.argv) == 2:
            mcbShelf.clear()
            # or use a for loop to clear elements one by one
        else:
            if sys.argv[2].lower() in mcbShelf:
                #mcbShelf.pop(sys.argv[2], None)
                del mcbShelf[sys.argv[2]]

    else:
        if sys.argv[1].lower() in mcbShelf:
            #print('answer of'+ {} +'is copied').format(str(sys.argv[1]))
            pyperclip.copy(str(mcbShelf[sys.argv[1]]))
        else:
            print('keyword is not found')
        pass


# TODO: List keywords and load content.

mcbShelf.close()