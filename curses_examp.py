import curses
import sys
import random
import time
import threading

class Chat:

    outputLines = []
    screen = None        
    def __init__(self):
        self.screen = curses.initscr()
        curses.echo()
        curses.cbreak()
        self.screen.keypad(1) 
        self.screen.border(0)
        self.topLineNum = 0
        self.nOutputLines=0

    def getIpt(self):
        return self.screen.getstr(0,0,curses.COLS)
        
    def run(self):
        while True:
            try:
                self.displayScreen()
                st = self.getIpt()
                if (st == ':q'):
                    break
                self.addLine(st)
            except: # catch *all* exceptions
                print(sys.exc_info())

    def addLine(self, line):
        self.outputLines.append(line)
        self.nOutputLines+=1
        if self.nOutputLines > curses.LINES -1:
            self.topLineNum += 1

    def displayScreen(self):
        self.screen.erase()
        top = self.topLineNum
        bottom = self.topLineNum+curses.LINES
        for (index,line,) in enumerate(self.outputLines[top:bottom]):
            linenum = self.topLineNum + index
            prefix = '___'
            line = '%s %s' % (prefix, line,)
            self.screen.addstr(index+1, 0, line)
        self.screen.refresh()
 
    def restoreScreen(self):
        curses.initscr()
        curses.nocbreak()
        curses.echo()
        curses.endwin()
    
    # catch any weird termination situations
    def __del__(self):
        self.restoreScreen()




if __name__ == '__main__':
    sys.stdout = open('err.txt', "w")
    ih = Chat()
    ih.run()



