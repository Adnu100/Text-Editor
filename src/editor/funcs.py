import curses

def initiate_curses():
    '''initiates curses nad returns an initialised _curses.window object with keypad(TRUE)'''
    stdscr = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    stdscr.clear()
    stdscr.move(0, 0)
    stdscr.refresh()
    return stdscr

def deinitiate_curses():
    '''resets the terminal to user-friendly settings and closes curses'''
    curses.echo()
    curses.nocbreak()
    curses.endwin()

def beepsound():
    curses.beep()
