# -*- coding: utf-8 -*-
"""
Usage:
  basic.py hello <argv1>
  # this defines the actual arguments, commands, etc.
  #use carefully
  
  basic.py (-h | --help)
Options:
  -h --help     Show this screen.

"""


from docopt import docopt

def greeter(arg):
    if arguments['hello']:
        print('hello '+str(arguments['<argv1>']))
    

if __name__ == '__main__':
    arguments = docopt(__doc__)
    
    print(arguments)
    # if an argument called hello was passed, execute the hello logic.
    greeter(arguments)