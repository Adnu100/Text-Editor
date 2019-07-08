#! /usr/bin/env python3

import sys
import curses
import editor

if __name__ == '__main__':
    '''driver code'''
    '''e = None
    try:'''
    if len(sys.argv) == 1:
        e = editor.Editor()
    else:
        e = editor.Editor(sys.argv[1])
    key = None
    while key != 'Q':
        key = e.getch()
        if key == curses.KEY_BACKSPACE:
            e.delchar()
        elif key == 10 or key == curses.KEY_ENTER:
            e.addtext('\n')
        else:
            e.addtext(chr(key & curses.A_CHARTEXT))
        key = chr(key & curses.A_CHARTEXT)
    e.close()
    '''except Exception as ex:
        if e:
            e.close()
        print("ERROR: ", end = '')
        print(ex)
    except:
        print("ERROR!")
    try:
        editor.deinitiate_curses()
    except Exception as e:
        print("ERROR: ", end = '')
        print(e)'''

