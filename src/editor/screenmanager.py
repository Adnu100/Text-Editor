import curses

from .funcs import *

from ._linebuffer import _LineBuffer

class Editor:
    '''editor class containing all methods to handle events'''
    __stdscr = None
    __instances = 0     # reserved to implement multiple files editing
    
    def __init__(self, filename = None):
        '''initiates the class, loads the file if given'''
        self.filename = filename
        Editor.__instances += 1
        if not Editor.__stdscr:
            Editor.__stdscr = initiate_curses()       # to ensure that curses is not initialised again
        self.updatewindowdimensions()
        self.lines = _LineBuffer(self.maxy, self.maxx)
        self.__running = True
        self._topln = 0
        if self.filename:
            self.load_from_file()

    def move_ahead(self, refresh = True): 
        '''moves the cursor ahead by one character'''
        y, x = self.__stdscr.getyx()
        case = self.lines.ahead()
        if case == 'a':
            x += 1
            if x == self.maxx:
                x = 0
                y += 1
            self.__stdscr.move(y, x)
        elif case == 'b':
            y += 1
            x = 0
            if y == self.maxy:
                self.updatescreen(1, cursor = "last")
                self.move_up(refresh = False)
                while self.move_ahead(refresh = False) != 'b': None
            else:
                self.__stdscr.move(y, 0)
        elif case == 'c':
            for _ in range(4):
                x += 1
                if x == self.maxx:
                    y += 1
                    x = 0
            self.__stdscr.move(y, x)
        elif case == 'd':
            beepsound()
            return
        if refresh:
            self.refresh()
        return case

    def move_back(self, refresh = True): 
        '''moves the cursor back by one character'''
        y, x = self.__stdscr.getyx()
        case = self.lines.back(self.maxx)
        if case == 'a':
            x -= 1
            if x == -1:
                y -= 1
                x = self.maxx - 1
            self.__stdscr.move(y, x)
        elif case == 'b':
            y -= 1
            x = self.lines.lastpos_cache
            if y == -1:
                self.updatescreen(-1, cursor = "start")
                self.move_down(refresh = False)
                self.move_back(refresh = False)
            else:
                self.__stdscr.move(y, x)
        elif case == 'c':
            for _ in range(4):
                x -= 1
                if x < 0:
                    y -= 1
                    x = self.maxx - 1
            self.__stdscr.move(y, x)
        elif case == 'd':
            beepsound()
            return
        if refresh:
            self.refresh()

    def move_up(self, refresh = True): 
        '''moves the cursor up by one line'''
        y, x = self.__stdscr.getyx()
        case = self.lines.up(self.maxx)
        if case == 'a':
            y -= self.lines.lineup_cache
            x = self.lines.cursorpos_cache
            if y < 0:
                self.updatescreen(-1, cursor = "start", set_cursor = False)
                y = self.lines.posline_cache
                x = self.lines.cursorpos_cache
                self.__stdscr.move(y, x)
            else:
                self.__stdscr.move(y, x)
        elif case == 'b':
            beepsound()
        if refresh:
            self.refresh()

    def move_down(self, refresh = True): 
        '''takes cursor down by one line'''
        y, x = self.__stdscr.getyx()
        case = self.lines.down(self.maxx)
        if case == 'a':
            y += self.lines.linedown_cache
            x = self.lines.cursorpos_cache
            if y >= self.maxy:
                self.updatescreen(1, cursor = "last", set_cursor = False)
                y, x = self.__stdscr.getyx()
                y -= self.lines.posline_cache
                x = self.lines.cursorpos_cache
                self.__stdscr.move(y, x)
            else:
                self.__stdscr.move(y, x)
        elif case == 'b':
            beepsound()
        if refresh:
            self.refresh()

    def addtext(self, ch, attr = curses.A_NORMAL, refresh = True): #to be done
        '''adds a character to the screen'''
        self.lines.add(ch, self.maxx)
        if ch != '\t':
            self.__stdscr.addstr(ch, attr)
        else:
            self.__stdscr.addstr("    ", attr)
        if refresh:
            self.refresh()
        pass

    def delchar(self, refresh = True): # partially done but workable under no move and no big file condition
        '''deletes a character from screen and refreshes screen'''
        y, x = self.__stdscr.getyx()
        case = self.lines.delete(self.maxx)
        if case == 'a' or case == 'b':
            range_ = 1 if case == 'a' else 4
            for _ in range(range_):
                self.__stdscr.delch()
                for i in range(self.lines.up_cache):
                    charinfo = self.__stdscr.inch(y + 1 + i, 0)
                    self.__stdscr.move(y + i, self.maxx - 1)
                    self.__stdscr.addstr(chr(charinfo & curses.A_CHARTEXT))
                    self.__stdscr.move(y + 1 + i, 0)
                    self.__stdscr.delch()
                self.__stdscr.move(y, x)
        elif case == 'c' or case == 'd':
            self.updatescreen(0, cursor = "current");
        else:
            beepsound()
        if refresh:
            self.refresh()

    def refresh(self): 
        '''refreshes the screen'''
        self.__stdscr.refresh()

    def clear(self, refresh = True):
        '''clears the screen'''
        self.__stdscr.clear()
        if refresh:
            self.refresh()

    def updatewindowdimensions(self):
        '''updates the window if size of window is changed, must be called when resize event occurs'''
        self.maxy, self.maxx = self.__stdscr.getmaxyx()
        self.maxy -= 1

    def close(self): 
        '''closes the current instance and deinitiates the curses if its the last instance'''
        if self.__running:
            self.__running = False
            Editor.__instances -= 1
            if Editor.__instances <= 0:
                self.__stdscr.keypad(0)
                deinitiate_curses()

    def save_to_file(self, filename = None): 
        '''saves the changes to the file
        if filename not provided, then uses the filename given at initialisation if given, else does nothing'''
        try:
            if filename == None:
                f = open(self.filename, 'r+')
            else:
                f = open(filename, 'r+')
        except FileNotFoundError:
            if filename == None:
                f = open(self.filename, 'w+')
            else:
                f = open(filename, 'w+')
        except:
            return False
        f.writelines(self.lines.lines)
        f.close()
        return True

    def load_from_file(self, filename = None): 
        '''loads the text from the filename
        if filename not provided, then uses the filename given at initialisation if given, else does nothing'''
        try:
            if filename == None:
                f = open(self.filename, 'r+')
            else:
                f = open(filename, 'r+')
        except:
            return False
        read = f.readlines()
        read[-1] = read[-1][:-1]
        self.lines = _LineBuffer(self.maxy, self.maxx, read)
        self.updatescreen()
        f.close()
        return True

    def updatescreen(self, movement = None, cursor = "last", set_cursor = True): 
        '''fills screen with the text in file, if file is too large to fit into the screen, it shows the last lines showable from file in the screen'''
        if movement != None:
            self._topln += movement
        else:
            self._topln = movement
        self.clear(refresh = False)
        line_list, self._topln = self.lines.getscreenlines(self.maxy, self.maxx, self._topln, cursor, set_cursor)
        for line in line_list:
            if '\t' in line:
                for ch in line:
                    if ch == '\t':
                        self.__stdscr.addstr("    ", curses.A_NORMAL)
                    else:
                        self.__stdscr.addstr(ch, curses.A_NORMAL)
            else:
                self.__stdscr.addstr(line, curses.A_NORMAL)
        if cursor == "start":
            self.__stdscr.move(0, 0)
        elif cursor == "current":
            self.__stdscr.move(*self.lines.getyxposition(self._topln, self.maxx))
        elif line_list[-1][-1] == '\n':
            self.move_back(refresh = False)
        self.refresh()

    def getch(self): 
        '''get a character from keyboard'''
        return self.__stdscr.getch()

    #def __del__(self): 
    #    '''assures that the close() function is called before the the object is deleted, or reference to the object is lost
    #    necessary to ensure that deinitiate_curses() is called before the program ends in order to return the terminal its settings before the program is called'''
    #    if self.__running:
    #        self.close()

