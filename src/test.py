#! /usr/bin/env python3

import sys
import curses
import editor

'''if __name__ == '__main__':
    e = None
    try:
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
            elif key == curses.KEY_LEFT:
                e.move_back()
            elif key == curses.KEY_RIGHT:
                e.move_ahead()
            else:
                e.addtext(chr(key & curses.A_CHARTEXT))
            key = chr(key & curses.A_CHARTEXT)
        e.close()
    except Exception as ex:
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
        print(e)
'''
if __name__ == '__main__':
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
            elif key == curses.KEY_LEFT:
                e.move_back()
            elif key == curses.KEY_RIGHT:
                e.move_ahead()
            else:
                e.addtext(chr(key & curses.A_CHARTEXT))
            key = chr(key & curses.A_CHARTEXT)
        e.close()

