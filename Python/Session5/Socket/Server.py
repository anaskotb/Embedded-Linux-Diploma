import socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip=socket.gethostbyname(socket.gethostname())
print(ip)
s.bind((ip,3000))
s.listen(5)
while True:
    c,addr=s.accept()
    print("connected to",addr)
    rodata=c.recv(1024)
    msg=str(input("please enter message you want to send to client"))
    message=msg.encode("utf-8")
    print(rodata.decode("utf-8"))
    c.send(message)
    c.close()

