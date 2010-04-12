'''
===========================================================

getch implementation
Sycamore

Copyright (C) 2010 Saumitro Dasgupta.

This code is made available under the MIT License.
<http://www.opensource.org/licenses/mit-license.html>

===========================================================

'''

import sys, tty, termios


'''
Unix-only getch implementation
'''

def getch():

    fn = sys.stdin.fileno()
    
    savedAttribs = termios.tcgetattr(fn)

    try:
        tty.setraw(fn)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fn, termios.TCSADRAIN, savedAttribs)

    return ch


'''
TODO : Add windows implementation
'''