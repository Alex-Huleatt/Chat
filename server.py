import socket,sys,time,threading,signal,re,random

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(0)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind the socket to the port
server_address = ('', int(input("Port:")))
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

nms = open('made_up.txt').read.split('\n')
random.shuffle(nms)
nms_index = 0
usr_nms = {}

queue = []
usrs = {}

def rec():
	global queue
	global usrs
	global usr_nms
	global nms_index
	r = re.compile('\s')
	while not kill:
		try:
			data, address = sock.recvfrom(4096)
		except:
			if (kill):
				return
			continue
		usrs[address]=time.time()
		if (address not in usr_nms):
			usr_nms[address]=nms[nms_index]
			nms_index= (nms_index+1)%len(nms)

		queue.append(re.sub('\n','',usr_nms[address]+':'+data.decode('UTF-8')))

def snd():
	global queue
	global usrs
	global usr_nms
	while not kill:
		toPop=[]
		if(len(queue)>0):
			d = queue.pop()
			t = time.time()
			if d:
				for u in usrs:
					if (t - usrs[u] > 1000):
						toPop.append(u)
					else:
						sent = sock.sendto(d, u)
		for u in toPop:
			usrs.pop(u,None)
			usr_nms.pop(u,None)

def signal_handler(signal, frame):
	global kill
	sock.close()
	kill = True
	sys.exit(0)


kill = False
def main():
	signal.signal(signal.SIGINT, signal_handler)
	t = threading.Thread(target=rec)
	t.start()
	snd()

main()