import socket
IP= "192.168.0.255"
PORT = 5005
MESSAGE  = "Thats just fucked up!"
sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto( MESSAGE, (IP,PORT))
sock.close()