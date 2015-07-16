import socket,sys,curses,random,time,threading,select,re



class Chat:
    outputLines = []
    screen = None
    curString = ''
    
    def __init__(self):
        self.screen = curses.initscr()
        curses.cbreak()
        curses.noecho()
        self.screen.keypad(1) 
        self.screen.border(0)
        self.topLineNum = 0
        self.nOutputLines=0
        self.displayScreen()

    def addLine(self, line):
        self.outputLines.append(line)
        self.nOutputLines+=1
        if self.nOutputLines > curses.LINES-1:
            self.topLineNum += 1

    def displayScreen(self):
        self.screen.erase()
        top = self.topLineNum
        bottom = self.topLineNum+(curses.LINES-1)
        self.screen.hline(0,0,'_',curses.COLS)
        self.screen.addstr(0, 0, self.curString)

        for (index,line,) in enumerate(self.outputLines[top:bottom]):
            linenum = self.topLineNum + index
            self.screen.addstr(index+1, 0, line)

        self.screen.move(0,len(self.curString))
        self.screen.refresh()

    def getCh(self):
        c = self.screen.getch()
        valid_chars = re.compile('[\w\s!\?\.\':;\[\],<>/"\+=\-_]') #valid character regex
        if c==ord('\n'):
            if len(self.curString)>0:
                t = self.curString
                self.curString=''
                self.displayScreen()
                return (1,t)
        elif c==ord('~'): #atilida kills the client
            return (-1,'')
        elif c in range(256) and not valid_chars.match(chr(c)): #if it isn't valid, it's a backspace
            self.curString=self.curString[:-1]
        elif (len(self.curString) < curses.COLS):
                self.curString+=chr(c)

        self.displayScreen()
        return (0,'')

def rec(cht,sock):
    global kill
    while not kill:
        try:
        	data, server = sock.recvfrom(4096)
        except:
        	continue
        cht.addLine(str(data))
        cht.displayScreen()
        

def send(cht,sock):
    global kill
    while 1:
        try: 
            ipt = cht.getCh()
            if ipt[0]==-1: #received ~, kill client
                sock.close()
                sys.stdout.close()
                curses.endwin()
                kill = True
                return
            elif ipt[0]==1:
                sent = sock.sendto(ipt[1], server_address)
        except:
            continue #sorrynotsorry

kill = False #global variable to alert for cleanup  

if __name__ == '__main__':
    port=int(input("Port:"))
    server_address = ('52.8.57.58', port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(0)
    sys.stdout = open('err.txt', "w")
    sys.stderr = sys.stdout
    ih = Chat()
    rec_th = threading.Thread(target=rec,args=(ih,sock))
    rec_th.start()
    send(ih,sock)
    rec_th.join()



