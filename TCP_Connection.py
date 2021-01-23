import Control
from socket import *

# Connection parameters
HOST='' # Everybody can connect
PORT=21555
BUFFSIZE=2048

ADDR=(HOST, PORT)
TCPServer_Socket=socket(AF_INET, SOCK_STREAM)
TCPServer_Socket.bind(ADDR)
TCPServer_Socket.listen()

def get_strength(y, z):
	strength=round(z,2)
	angle=round(y*90/9.8,0)
	return [strength,angle]

def drive_from_phone(speed, angle):
	'''
	Handle the data received from the phone.
	Speed and Angle are between -10 and 10 (approx)
	'''
	print("Speed: " + str(speed) + "\nAngle: " + str(angle))

	speed = speed * 25
	speed = 255 if speed > 255 else speed # Cap off at maximum

	if (angle > 2.5):
		direction = 'RIGHT'
		strength = 30
	elif (angle < 2.5):
		direction = 'LEFT'
		strength = 30
	else:
		direction = 'STRAIGHT'
		strength = 0

	Control.drive(int(speed), direction, int(strength))

print("Opened a connection on port "+ str(PORT))

while True:
	try:
		#print("Waiting for connection ...")
		conn,addr=TCPServer_Socket.accept()
		#print("Connection established to "+str(addr))
		while True:
			data=''
			data=conn.recv(BUFFSIZE).decode('ascii')
			if not data:
				break
			else:
				#do something with the data received
				list_data = data.split(",")
				if (len(list_data) == 3 and len(list_data[1]) > 2 and len(list_data[2]) > 2):
					drive_from_phone(float(list_data[2]), float(list_data[1]))
	except KeyboardInterrupt:
		print("\n\n===== \nClosed")
		TCPServer_Socket.close()
		break;
