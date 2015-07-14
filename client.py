import socket,sys,curses,random,time,threading,select

kill = False

class Chat:
    outputLines = []
    screen = None
    curString = ''
       
    def __init__(self):
        self.screen = curses.initscr()
        curses.cbreak()
        self.screen.keypad(1) 
        self.screen.border(0)
        self.topLineNum = 0
        self.nOutputLines=0
        self.displayScreen()

    def addLine(self, line):
        self.outputLines.append(line)
        self.nOutputLines+=1
        if self.nOutputLines > curses.LINES -1:
            self.topLineNum += 1

    def displayScreen(self):
        self.screen.erase()
        top = self.topLineNum
        bottom = self.topLineNum+curses.LINES
        self.screen.addstr(0, 0, self.curString)
        for (index,line,) in enumerate(self.outputLines[top:bottom]):
            linenum = self.topLineNum + index
            self.screen.addstr(index+1, 0, line)
        self.screen.move(0,len(self.curString))
        self.screen.refresh()
 
    def restoreScreen(self):
        curses.initscr()
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def getCh(self):
        c = self.screen.getch()
        print('read:',c)
        if c==ord('\n'):
            self.curString=''
        elif c==ord('~'):
            return -1
        else:
            self.curString+=chr(c)

        self.displayScreen()
        return c
    
    # catch any weird termination situations
    def __del__(self):
        self.restoreScreen()

def rec(cht,sock):
    global kill
    while not kill:
        # Receive response
        try:
        	data, server = sock.recvfrom(4096)
        except:
        	continue
        print('received "%s"' % data)
        cht.addLine(str(data))
        cht.displayScreen()
        

def send(cht,sock):
    global kill
    while 1:
        while 1:
            ipt = cht.getCh()
            if ipt==-1:
                sock.close()
                kill = True
                return

        # Send data
        print('sending "%s"' % read)
        sent = sock.sendto(read, server_address)



if __name__ == '__main__':
    port=int(input("Port:"))
    server_address = ('52.8.57.58', port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(0)
    sys.stdout = open('err.txt', "w")
    sys.stderr = sys.stdout
    ih = Chat()
    rec_th = threading.Thread(target=rec,args=(ih,sock) )
    rec_th.start()
    send(ih,sock)
    sys.exit()



