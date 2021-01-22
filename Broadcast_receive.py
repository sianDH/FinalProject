import socket
IP   = "192.168.0.255"
PORT = 5005
sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind( (IP,PORT))

while True:
  data, addr = sock.recvfrom(1024)
  print "Received Data:", data