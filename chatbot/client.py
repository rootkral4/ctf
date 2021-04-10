import socket


username = "hakanbey:"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(("127.0.0.1", 1234))
except:
    print("Connection Refused")
    exit()
def sendnreceive():
    try:
        s.send("CLIENT".encode())
        s.send(input("PASSWORD :").encode())
    except:
        print("Connection Refused")
        exit()
    print(s.recv(4096).decode())
    while 1:
        msg2send = input("->")
        print(username + msg2send)
        s.send(msg2send.encode())
        recvmsg = s.recv(4096).decode()
        print(recvmsg)
        if "kral4 disconnected" in recvmsg.strip():
            print("connection terminated")
            break

sendnreceive()
