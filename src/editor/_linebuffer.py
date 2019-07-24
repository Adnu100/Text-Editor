NEWLINE = '\n'
TAB = '\t'

class _LineBuffer:
    '''stores mulitple lines in a list data structure'''

    def __init__(self, maxy, maxx, l = []):
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
        self.fwr = True

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
                if self.curch == len(self.lines[self.curline]):
                    return 'd'
                else:
                    self.curch += 1
                    return 'a' if self.lines[self.curline][self.curch - 1] != TAB else 'c'
            else:
                self.curch += 1
                if self.curch == len(self.lines[self.curline]):
                    self.curline += 1
                    self.curch = 0
                    return 'b'
                return 'a' if self.lines[self.curline][self.curch - 1] != TAB else 'c'
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

    def up(self, mx):
        '''sets the focus on the upper line
        returns either of 'a' and 'b' depending on the conditions:
            a : when the cursor can be moved to the upper line (the number of lines by which the cursor needs to go up is stored in lineup_cache while the cursor x position is stored in cursorpos_cache
            B : when the cursor can not be moved up'''
        if self.lines:
            if self.curline != 0:
                pos1 = len(self.lines[self.curline][:self.curch]) + self.lines[self.curline][:self.curch].count(TAB) * 3
                pos1_line = pos1 // mx + 1
                self.lineup_cache = pos1_line
                l = len(self.lines[self.curline - 1])
                if self.curch >= l:
                    self.curch = l - 1
                pos2 = len(self.lines[self.curline - 1][:self.curch]) + self.lines[self.curline - 1][:self.curch].count(TAB) * 3
                pos2_line = pos2 // mx + 1
                pos2_line = self.required_lines[self.curline - 1] - pos2_line
                self.lineup_cache += pos2_line
                self.cursorpos_cache = pos2 % mx
                self.curline -= 1
                return 'a'
        return 'b'

    def down(self, mx):
        '''sets the focus onw line down
        returns either of 'a' and 'b' depending on conditions:
            a : when the cursor can be moved down (the number of lines the cursor needs to be shifted down is stored in linedown_cache while the cursor position is stored in cursorpos_cache
            b : when the cursor can not be moved down'''
        if self.lines:
            if self.curline != len(self.lines) - 1:
                pos1 = len(self.lines[self.curline][:self.curch]) + self.lines[self.curline][:self.curch].count(TAB) * 3
                pos1_line = pos1 // mx + 1
                self.linedown_cache = self.required_lines[self.curline] - pos1_line
                l = len(self.lines[self.curline + 1])
                if self.curch >= l:
                    self.curch = l - 1
                pos2 = len(self.lines[self.curline + 1][:self.curch]) + self.lines[self.curline + 1][:self.curch].count(TAB) * 3
                pos2_line = pos2 // mx + 1
                self.linedown_cache += pos2_line
                self.cursorpos_cache = pos2 % mx
                self.curline += 1
                return 'a'
        return 'b'

    def add(self, ch, maxx):
        '''adds a character to the current line at the index curch (current character)'''
        if self.lines:
            if ch != NEWLINE:
                self.lines[self.curline] = self.lines[self.curline][:self.curch] + ch + self.lines[self.curline][self.curch:]
                self.lens[self.curline] = (self.lens[self.curline] + 1) if ch != TAB else (self.lens[self.curline] + 4)
                self.required_lines[self.curline] = (self.lens[self.curline] // maxx) + 1
            else:
                temp = self.lines[self.curline][:self.curch] + NEWLINE
                self.lines.insert(self.curline + 1, self.lines[self.curline][self.curch:])
                self.lens.insert(self.curline + 1, len(self.lines[self.curline + 1]) + 3 * self.lines[self.curline].count(TAB))
                self.lens[self.curline] = len(temp) + 3 * temp.count(TAB)
                self.lines[self.curline] = temp
                self.required_lines[self.curline] = (self.lens[self.curline] // maxx) + 1
                self.required_lines.insert(self.curline + 1, (self.lens[self.curline] // maxx) + 1)
                self.curline, self.curch = self.curline + 1, -1
        else:
            self.lines.append(ch)
            self.lens.append(len(ch.expandtabs(4)))
            self.required_lines.append((len(ch.expandtabs(4)) // maxx) + 1)
        self.curch += 1

    def filewriter(self):
        '''a function which writes all the log in debug.txt file
        use this function for debugging purposes'''
        if self.fwr:
            self.__f = open("debug.txt", "w+")
            self.fwr = False
        for x__x in self.lines:
            self.__f.write(list(x__x).__str__() + NEWLINE)
        self.__f.write(f"curchar- {self.curch}, curline - {self.curline}")
        self.__f.write('\n\n')

    def close(self):
        '''close the debug.txt file after this object is closed'''
        self.__f.close()

    def delete(self):
        pass

