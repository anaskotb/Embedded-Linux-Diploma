import socket
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip=socket.gethostbyname(socket.gethostname())
client.connect((ip,3000))
msg=str(input("please enter message to server"))
client.send(msg.encode("utf-8"))

rodata=client.recv(1024)
print(rodata.decode("utf-8"))
client.close()
