from socket import *
#everybody can connect
HOST='' 
PORT=21555
BUFFSIZE=2048
ADDR=(HOST,PORT)
TCPServer_Socket=socket(AF_INET,SOCK_STREAM)
TCPServer_Socket.bind(ADDR)
TCPServer_Socket.listen()

def get_strength(y,z):
  strength=round(z,2)
  angle=round(y*90/9.8,0)
  return [strength,angle]

while True:
    print("Waiting for connection ...")
    conn,addr=TCPServer_Socket.accept()
    print("Connection established to "+str(addr))
    try:
        while True:
           data=''
           data=conn.recv(BUFFSIZE).decode('ascii')
           if not data:
                break
           else:
                #do something with the data received
                list_data=data.split(",")
                if(len(list_data)==3):
                  print(get_strength(float(list_data[1]),float(list_data[2])))
                  #do something with data from get_strenth firts one is the power and second is the angle
    except KeyboardInterrupt:
        print("Closed")
TCPServer_Socket.close()
