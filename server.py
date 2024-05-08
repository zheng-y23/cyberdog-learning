import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 40008 #use your own port

serversocket.bind((host,port))
serversocket.listen(5)

while True:
    clientsocket, addr = serversocket.accept()
    print("连接地址：%s" % str(addr))
    msg = 'hello cyberdog!!' + '\n'
    clientsocket.send(msg.encode())
    clientsocket.close()
