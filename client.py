import socket
import sys
import curses
stdscr = curses.initscr()

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


server_address = ('localhost', 10000)


try:
	while(1):
		message = input(':')
	    # Send data
	    print >>sys.stderr, 'sending "%s"' % message
	    sent = sock.sendto(message, server_address)

	    # Receive response
	    print >>sys.stderr, 'waiting to receive'
	    data, server = sock.recvfrom(4096)
	    print >>sys.stderr, 'received "%s"' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()