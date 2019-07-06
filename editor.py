from funcs import *

NEWLINE = '\n'
TAB = '\t'

class _LineBuffer:
    '''stores mulitple lines in a list data structure'''
    def __init__(self, l = [], curr = 0):
        self.lines = l
        pass
    
    def getscreenlines(self, my, mx):
        pass

    def ahead(self):
        pass

    def back(self):
        pass

    def up(self):
        pass

    def down(self):
        pass

    def add(self, ch):
        pass

    def delete(self):
        pass

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
        self.lines = _LineBuffer()
        self.__running = True
        if self.filename:
            self.load_from_file()

    def move_ahead(self, characters = 1, refresh = True): #done
        '''moves the cursor ahead by given number of characters'''
        y, x = self.__stdscr.getyx()
        y, x = self.lines.ahead(characters, y, x, self.maxy, self.maxx)
        if x != None and y != None:
            self.__stdscr.move(self.cury, self.curx)
        if refresh:
            self.refresh()

    def move_back(self, characters = 1, refresh = True): #done
        '''moves the cursor back by given number of characters'''
        y, x = self.__stdscr.getyx()
        y, x = self.lines.back(characters, y, x, self.maxy, self.maxx)
        if x != None and y != None:
            self.__stdscr.move(y, x)
        if refresh:
            self.refresh()

    def move_up(self, by = 1, refresh = True): #done
        '''moves the cursor up by given lines'''
        y, x = self.__stdscr.getyx()
        y, x = self.lines.up(by, y, x, self.maxy, self.maxx)
        if x != None and y != None:
            self.__stdscr.move(y, x)
        if refresh:
            self.refresh()
        pass

    def move_down(self, by = 1, refresh = True): #done
        '''takes cursor down by given lines'''
        y, x = self.__stdscr.getyx()
        y, x = self.lines.down(by, y, x, self.maxy, self.maxx)
        if x != None and y != None:
            self.__stdscr.move(y, x)
        if refresh:
            self.refresh()
        pass

    def addtext(self, ch, attr = curses.A_NORMAL, refresh = True): # partially done but workable under no move conditions
        if self.lines.add(ch):
            self.__stdscr.addstr(ch, attr)
        else:
            pass
        if refresh:
            self.refresh()
        pass

    def delchar(self, refresh = True): # partially done but workable under no move and no big file condition
        '''deletes a character from screen and refreshes screen'''
        self.move_back(refresh = False)
        c = self.lines.delete()
        if c == 0:
            self.__stdscr.delch()
        else:
            pass
        if refresh:
            self.refresh()
        pass

    def refresh(self): #done
        '''refreshes the screen'''
        self.__stdscr.refresh()

    def clear(self, refresh = True): #done
        '''clears the screen'''
        self.__stdscr.clear()
        if refresh:
            self.refresh()

    def updatewindowdimensions(self): #done
        '''updates the window if size of window is changed, must be called when resize event occurs'''
        self.maxy, self.maxx = self.__stdscr.getmaxyx()

    def close(self): #done
        '''closes the current instance and deinitiates the curses if its the last instance'''
        if self.__running:
            self.__running = False
            Editor.__instances -= 1
            if Editor.__instances <= 0:
                self.__stdscr.keypad(0)
                deinitiate_curses()

    def save_to_file(self, filename = None): #done
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

    def load_from_file(self, filename = None): #done
        '''loads the text from the filename
        if filename not provided, then uses the filename given at initialisation if given, else does nothing'''
        try:
            if filename == None:
                f = open(self.filename, 'r+')
            else:
                f = open(filename, 'r+')
        except:
            return False
        self.lines = _LineBuffer(f.readlines())
        self.updatescreen()
        f.close()
        return True

    def updatescreen(self): #done
        '''fills screen with the text in file, if file is too large to fit into the screen, it shows the last lines showable from file in the screen'''
        self.clear(refresh = False)
        line_list = self.lines.getscreenlines(self.maxy, self.maxx)
        for line in line_list:
            self.__stdscr.addstr(line, curses.A_NORMAL)
        self.refresh()

    def getch(self): #done
        '''get a character from keyboard'''
        return self.__stdscr.getch()

    def __del__(self): #done
        '''assures that the close() function is called before the the object is deleted, or reference to the object is lost
        necessary to ensure that deinitiate_curses() is called before the program ends in order to return the terminal its settings before the program is called'''
        if self.__running:
            self.close()

