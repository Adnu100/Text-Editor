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
        self.lens = [len(line) + (line.count(TAB) * 3) for line in self.lines]
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
            c: when the cursor has to be moved by a tab
            d: when the cursor can not be moved'''
        if self.lines:
            if self.curline == len(self.lines) - 1:
                if self.curch == len(self.lines[self.curch]):
                    return 'd'
                else:
                    self.curch += 1
                    return 'a' if self.lines[self.curline][self.curch - 1] != TAB else 'c'
            else:
                self.curch += 1
                if self.lines[self.curline][self.curch] == NEWLINE:
                    self.curline += 1
                    self.curch = 0
                    return 'b'
                return 'a'if self.lines[self.curline]pself.curch - 1] != TAB else 'c'
        else:
            return 'd'

    def back(self, maxx):
        '''sets the focus on previous character, same as _LineBuffer.ahead()
        returns either of 'a', 'b', 'c' depending on conditions:
            a : when the cursor can be moved
            b : when the cursor has to be moved one line above (the last character position is stored in lastpos_cache)
            c : when the cursor has to be moved by a tab
            d : when the cursor can not be moved'''
        if self.lines:
            if self.curline == 0:
                if self.curch == 0:
                    return 'd'
                else:
                    self.curch -= 1
                    if self.lines[self.curline][self.curch] == TAB:
                        return 'c'
                    else:
                        return 'a'
            else:
                if self.curch == 0:
                    self.curline -= 1
                    self.curch = len(self.lines[self.curline]) - 1
                    l = self.lens[self.curline]
                    lm = self.required_lines[self.curline] * maxx
                    self.lastpos_cache = (maxx - (lm - l)) - 1
                    return 'b'
                else:
                    self.curch -= 1
                    if self.lines[self.curline][self.curch] == TAB:
                        return 'c'
                    else:
                        return 'a'
        else:
            return 'd'

    def up(self):
        pass

    def down(self):
        pass

    def add(self, ch):
        if self.lines:
            if ch != NEWLINE:
                self.lines[self.curline] = self.lines[self.curline][:self.curch] + ch + self.lines[self.curline][self.curch:]
                self.lens[self.curline] = (self.lens[self.curline] + 1) if ch != TAB else (self.lens[self.curline] + 4)
            else:
                temp = self.lines[self.curline][:self.curch] + NEWLINE
                if self.curch != len(self.lines[self.curline]):
                    self.lines.insert(self.curline + 1, self.lines[self.curline][self.curch:])
                    self.lens.insert(self.curline + 1, len(self.lines[self.curline + 1].expandtabs(4)))
                    self.lens[self.curline] = len(temp.expandtabs(4))
                self.lines[self.curline] = temp
        else:
            self.lines.append(ch)
        return self.ahead()

    def delete(self):
        pass

