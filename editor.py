from funcs import *

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
        self.curx = 0
        self.cury = 0
        self.updatewindowdimensions()
        self.lines = []
        self.__running = True
        if filename == None or not self.load_from_file():
            self.__current_lines = [0, 0]

    def __move_ahead(self, characters = 1):
        '''moves the cursor ahead by given number of characters'''
        for _ in range(characters):
            self.curx += 1
            if self.curx == self.maxx:
                self.curx = 0
                self.cury += 1
                if self.cury == self.maxy:
                    return
                    pass
        self.__stdscr.move(self.cury, self.curx)

    def __move_back(self, characters = 1):
        '''moves the cursor back by given number of characters'''
        for _ in range(characters):
            self.curx -= 1
            if self.curx < 0:
                self.curx = self.maxx - 1
                self.cury -= 1
                if self.cury < 0:
                    pass
        self.__stdscr.move(self.cury, self.curx)

    def addtext(self, ch, attr = curses.A_NORMAL, y = None, x = None, refresh = True):
        if x == None or y == None:
            x, y = self.curx, self.cury
        else:
            self.__stdscr.move(y, x)
        self.__stdscr.addstr(y, x, ch, attr)
        self.__move_ahead(len(ch))
        if refresh:
            self.refresh()
        pass

    def delchar(self, y = None, x = None, refresh = True):
        '''deletes a character from screen and refreshes screen'''
        if x == None or y == None:
            self.__move_back()
        else:
            self.__stdscr.move(y, x)
        self.__stdscr.delch()
        if refresh:
            self.refresh()
        pass

    def newline(self, refresh = True):
        '''adds a newline character, moves the cursor to the newline'''
        self.curx = 0
        self.cury += 1
        if self.cury == self.maxy:
            pass
        self.__stdscr.move(self.cury, self.curx)
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
        pass

    def load_from_file(self, filename = None):
        '''loads the text from the filename
        if filename not provided, then uses the filename given at initialisation if given, else does nothing'''
        try:
            f = open(self.filename, 'r+')
        except:
            return False
        self.lines = f.readlines()
        c = d = 0
        for line in self.lines:
            c += ((len(line) // self.maxx) + 1)
            d += 1
            if c >= self.maxy:
                break
        self.__current_lines = [0, d - 1]
        self.updatescreen()
        f.close()
        return True

    def updatescreen(self):
        self.clear(refresh = False)
        for line in self.lines[self.__current_lines[0]:self.__current_lines[1]]:
            self.addtext(line[:-1], refresh = False)
            self.newline(refresh = False)
        self.addtext(self.lines[self.__current_lines[1]][:self.maxx], refresh = False)
        self.refresh()

    def getch(self):
        '''get a character from keyboard'''
        return self.__stdscr.getch()

    def __del__(self):
        '''assures that the close() function is called before the the object is deleted, or reference to the object is lost
        necessary to ensure that deinitiate_curses() is called before the program ends in order to return the terminal its settings before the program is called'''
        if self.__running:
            self.close()

