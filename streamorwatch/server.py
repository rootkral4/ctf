import threading
import socket
import zlib

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 1212))
s.listen()

is_already_streaming = False
streamerc = []
watchersc = []
getstreamandbroadcast_kill = False
accept_kill = False
clist = []


def threadhandler(lockname, value=1):
    """
    :lockname: name of setting
    :value: int, 1 = True 0 = False
    """
    global getstreamandbroadcast_kill
    global accept_kill
    if lockname == "getstreamandbroadcast_kill":
        if value == 1:
            getstreamandbroadcast_kill = True
        elif value == 0:
            getstreamandbroadcast_kill = False
    elif lockname == "accept_kill":
        if value == 1:
            accept_kill = True
        elif value == 0:
            accept_kill = False

def getstreamandbroadcast():
    global is_already_streaming
    while getstreamandbroadcast_kill == False:
        try:
            lenghtofdata = streamerc.recv(4096).decode().strip()
            lenghtofdata = int(lenghtofdata)
            data = b""
            while True:
                if len(data) >= lenghtofdata:
                    break
                else:
                    newdata = streamerc.recv(4096)
                    data += newdata
            threading.Thread(target=stream, args=(data,)).start()
        except ConnectionResetError:
            is_already_streaming = False
            streamerc.clear()
        except ValueError:
            is_already_streaming = False
            streamerc.clear()

def stream(data):
    for c in watchersc:
        try:
            c.sendall(str(len(data)).encode())
            c.sendall(data)
        except Exception as e:
            print(e)
            watchersc.remove(c)
            pass

def accept(s):
    while accept_kill == False:
        c, addr = s.accept()
        clist.append(c)
        threading.Thread(target=handleclient, args=(c,), name="handle_client_" + str(len(clist))).start()

def handleclient(c):
    global is_already_streaming
    while True:
        try:
            client_type = c.recv(4096).decode().strip()
        except ConnectionResetError:
            clist.remove(c)
            pass
            break
        if client_type == "STREAMER":
            if is_already_streaming:
                c.sendall("ALREADY_STREAMING".encode())
            else:
                is_already_streaming = True
                threading.Thread(target=servetoclient, args=(c, client_type), name="serve_client_" + str(len(clist))).start()
                break
        elif client_type == "WATCHER":
            if is_already_streaming:
                c.sendall("WELCOME".encode())
                threading.Thread(target=servetoclient, args=(c, client_type), name="serve_client_" + str(len(clist))).start()
                break
            else:
                c.sendall("NO_STREAM".encode())
        elif client_type == "PING":
            c.sendall("PONG".encode())

def servetoclient(c, client_type):
    global streamerc
    if client_type == "WATCHER":
        watchersc.append(c)
    elif client_type == "STREAMER":
        streamerc = c
        clist.remove(streamerc)
        streamerc.sendall("WELCOME".encode())
        threading.Thread(target=getstreamandbroadcast, name="handle_streamer").start()

def admin(s):
    global is_already_streaming
    helpmenu = """
    start
    stop
    show_status
    kick_streamer
    kick_client IP
    """
    print(helpmenu)
    while True:
        command = input("->")
        command = command.split(" ")
        if command[0] == "start":  
            threadhandler("accept_kill", 0)
            threading.Thread(target=accept, args=(s,)).start()
        elif command[0] == "stop":
            threadhandler("accept_kill")
        elif command[0] == "exit":
            threadhandler("accept_kill")
            threadhandler("get_streamandbroadcast_kill")
            break
        elif command[0] == "show_status":
            print("Total :",len(watchersc),"clients connected")
            print("streamer :",is_already_streaming)
            print(watchersc)
            if is_already_streaming:
                print(streamerc)
        elif command[0] == "kick_streamer":
            threadhandler("getstreamandbroadcast_kill", 1)
            is_already_streaming = False
            streamerc.clear()
        elif command[0] == "kick_client":
            for cl in watchersc:
                if command[1] in str(cl):
                    cl.close()
                    watchersc.remove(cl)
        
admin(s)
