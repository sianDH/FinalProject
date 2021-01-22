from socket import *
#everybody can connect
HOST='' 
PORT=21555
BUFFSIZE=2048
ADDR=(HOST,PORT)
TCPServer_Socket=socket(AF_INET,SOCK_STREAM)
TCPServer_Socket.bind(ADDR)
TCPServer_Socket.listen()
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
                print(list_data)
    except KeyboardInterrupt:
        print("Closed")
TCPServer_Socket.close()
