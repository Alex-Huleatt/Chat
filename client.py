import socket,sys,curses,random,time,threading,select

kill = False

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
        self.displayScreen()

    def getIpt(self):
        return self.screen.getstr(0,0,curses.COLS)
        
    def run(self):
        global kill
        while not kill:
            try:
                self.displayScreen()
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
        self.screen.move(0,0)
        self.screen.refresh()
 
    def restoreScreen(self):
        curses.initscr()
        curses.nocbreak()
        curses.echo()
        curses.endwin()
    
    # catch any weird termination situations
    def __del__(self):
        self.restoreScreen()

def rec(cht,sock):
    global kill
    while not kill:
        # Receive response
        print('waiting to receive')
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
        ipt = cht.getIpt()
        if (ipt == ':q'):
            kill=True
            break
        # Send data
        print('sending "%s"' % ipt)
        sent = sock.sendto(ipt, server_address)
        cht.displayScreen()
    print(sys.stderr, 'closing socket')
    sock.close()



if __name__ == '__main__':
    server_address = ('52.8.57.58', 40001)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(0)
    sys.stdout = open('err.txt', "w")
    sys.stderr = sys.stdout
    ih = Chat()
    rec_th = threading.Thread(target=rec,args=(ih,sock) )
    rec_th.start()
    send(ih,sock)



