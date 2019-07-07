from funcs import *

NEWLINE = '\n'
TAB = '\t'

class _LineBuffer:
    '''stores mulitple lines in a list data structure'''
    def __init__(self, maxy, maxx, l = [], curr = 0):
        '''initialises the LineBuffer'''
        self.lines = l
        if l:
            self.curline = len(self.lines) - 1
            self.curch = len(self.lines[self.curline])
        else:
            self.curline = 0
            self.curch = 0
        self.lens = [len(line.expandtabs(4)) for line in self.lines]
        self.setup(maxx)

    def setup(self, mx):
        '''sets the required lines on screen to display the actual line in file for each line'''
        self.required_lines = [(i // mx) + 1 for i in self.lens]
    
    def getscreenlines(self, my, mx, pos = None):
        '''returns the maximum lines to be shown on screen'''
        if pos == None:
            c = sum_ = 0
            for i in self.required_lines[::-1]:
                sum_ += i
                if sum_ > my:
                    break
                c += 1
            return self.lines[-c:]
        else:
            c = sum_ = 0
            for i in self.required_lines[pos:]:
                sum_ += i
                if sum_ > my:
                    c +=1 
            return self.lines[pos:pos + c]

    def ahead(self):
        '''sets the focus to next character, also returns the cases to set cursor position
        returns either of 'a', 'b', 'c' based on the condition:
            a: when the cursor can be moved
            b: when the cursor has to be moved to newline
            c: when the cursor can not be moved'''
        if self.lines:
            if self.curline == len(self.lines) - 1:
                if self.curch == len(self.lines[self.curch]):
                    return 'c'
                else:
                    self.curch += 1
                    return 'a'
            else:
                self.curch += 1
                if self.lines[self.curline][self.curch] == '\n':
                    self.curline += 1
                    self.curch = 0
                    return 'b'
                return 'a'
        else:
            return 'c'

    def back(self, maxx):
        '''sets the focus on previous character, same as _LineBuffer.ahead()
        returns either of 'a', 'b', 'c' depending on conditions:
            a: when the cursor can be moved
            b: when the cursor has to be moved one line above (the last character position is stored in lastpos_cache
            c: wehn the cursor can not be moved'''
        if self.lines:
            if self.curline == 0:
                if self.curch == 0:
                    return 'c'
                else:
                    self.curch -= 1
                    return 'a'
            else:
                if self.curch == 0:
                    self.curline -= 1
                    self.curch = len(self.lines[self.curline]) - 2
                    l = len(self.lines[self.curline])
                    lm = self.required_lines[self.curline] * maxx
                    self.lastpos_cache = (maxx - (lm - l)) - 1
                    return 'b'
                else:
                    self.curch -= 1
                    return 'a'
        else:
            return 'c'

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
        case = self.lines.ahead(characters)
        if case == 'a':
            x += 1
            if x == self.maxx:
                x = 0
                y += 1
            if y == self.maxy:
                pass
            self.__stdscr.move(y, x)
        elif case == 'b':
            y += 1
            x = 0
            if y == self.maxy:
                pass
            self.__stdscr.move(y + 1, 0)
        elif case == 'c':
            curses.beep()
            return
        if refresh:
            self.refresh()

    def move_back(self, characters = 1, refresh = True): #done
        '''moves the cursor back by given number of characters'''
        y, x = self.__stdscr.getyx()
        case = self.lines.back(characters, self.maxx)
        if case == 'a':
            x -= 1
            if x == -1:
                y -= 1
                x = self.maxx - 1
            if y == -1:
                pass
            self.__stdscr.move(y, x)
        elif case == 'b':
            y -= 1
            x = self.lastpos_cache
            if y == -1:
                pass
            self._stdscr.move(y, x)
        elif case == 'c':
            curses.beep()
            return
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
        self.lines.add(ch):
        if pass:
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

