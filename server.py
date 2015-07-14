import socket,sys,time,threading,signal




# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind the socket to the port
server_address = ('', int(input("Port:")))
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

queue = []
usrs = {}

def rec():
	global queue
	global usrs
	while 1:
		data, address = sock.recvfrom(4096)
		usrs[address]=time.time()
		print(data)
		queue.append(data)

def snd():
	global queue
	global usrs
	while 1:
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

def signal_handler(signal, frame):
	sock.close()
	sys.exit(0)

def main():
	signal.signal(signal.SIGINT, signal_handler)
	t = threading.Thread(target=rec)
	t.start()
	snd()

main()