import socket,sys,time,threading

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind the socket to the port
server_address = ('', 40000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# while True:
#     print >>sys.stderr, '\nwaiting to receive message'
#     data, address = sock.recvfrom(4096)
    
#     print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
#     print >>sys.stderr, data
    
#     if data:
#         sent = sock.sendto(data, address)
#         print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)

queue = []
usrs = {}

def rec():
	global queue
	global usrs
	while 1:
		data, address = sock.recvfrom(4096)
		usrs[address]=time.time()
		queue.append(data)

def snd():
	global queue
	global usrs
	while 1:
		if(len(queue)>0):
			d = queue.pop()
			t = time.time()
			if d:
				for u in usrs:
					if (t - usrs[u] > 1000):
						usrs.pop(u,None)
					else:
						sent = sock.sendto(d, u)

def main():
	t = threading.Thread(target=rec)
	t.start()
	snd()

main()