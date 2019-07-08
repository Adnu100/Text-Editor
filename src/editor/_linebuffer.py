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
                if self.lines[self.curline][self.curch] == NEWLINE:
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
            b: when the cursor has to be moved one line above (the last character position is stored in lastpos_cache)
            c: when the cursor has to be moved by a tab, the x-shift is stored in x_shift_cache
            d: wehn the cursor can not be moved'''
        if self.lines:
            if self.curline == 0:
                if self.curch == 0:
                    return 'd'
                else:
                    self.curch -= 1
                    if self.lines[self.curline][self.curch] == TAB:
                        pass
                        return 'c'
                    else:
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
            return 'd'

    def up(self):
        '''sets the focus on the earlier line, character focus remains same is the line is lengthy enough, otherwise the character focus decreases to the greatest value it has
        returns either of 'a', 'b', 'c', 'd' depending on conditions:
            a: when the cursoe can be safely moved up
            b: when the cursor can be safely moved up and requires to be moved more than one line up (the number of lines is stored in y_shift_cache
            c: when cursor can be safely moved up but requires x-shift (the x-shift is stored in x-shift cache)
            d: when the cursor can not be moved'''
        if self.lines:
            if self.curline == 0:
                return 'd'
            else:
                pass 
        else:
            return 'd'
        pass

    def down(self):
        pass

    def add(self, ch):
        pass

    def delete(self):
        pass


