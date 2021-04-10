import socket
import threading
import time

username = "kral4:"
password = "Mys3cr3tp4sw0rD"
passwordtoconnect = "MBMD1vdpjg3kGv6SsIz56VNG"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(("127.0.0.1", 1234))
s.listen()

clist = []
addrlist = []

answers = {
    "1": username + "hi hakanbey\n",
    "2": username + "how are you?\n",
    "3": username + "what now? did you forgot your password again\n",
    "4": username + "okay your password is " + password + " don't lose it PLEASE\n"
}

def checkisclient(c):
    data = c.recv(4096).decode().strip()
    if data == "CLIENT":
        if c.recv(4096).decode().strip() == passwordtoconnect:
            return True
        else:
            return False
    else:
        return False

def accept():
    global clist
    global addrlist
    while 1:
        if not isfirst():
            break
        c, addr = s.accept()
        if not isfirst():
            break
        if checkisclient(c):
            clist.append(c)
            addrlist.append(addr)
            threading.Thread(target=handle_client, args=(c,)).start()
        else:
            c.sendall("NOT AUTHORIZED".encode())
            c.close()

def answer(c, msg):
    msg = msg.lower()
    if msg == "hi" or msg == "hello":
        time.sleep(2)
        c.sendall(answers["2"].encode())
    elif any(x in msg for x in ("thanks", "fine", "good", "bad", "happy", "hungry")):
        time.sleep(5)
        c.sendall(answers["3"].encode())
    elif any(x in msg for x in ("yes", "yeah", "yup")):
        lastmsg = answers["4"] + "kral4:i have to go\n" + "kral4 disconnected\n"
        time.sleep(6)
        c.sendall(lastmsg.encode())
        time.sleep(2)
        c.close()
        with open("/home/kral4/.check", "w") as f:
            f.write("False")

    else:
        c.sendall("?\n".encode())
      
def handle_client(c):
    time.sleep(2)
    c.sendall(answers["1"].encode())
    while 1:
        try:
            msg = c.recv(4096).decode().strip()
            answer(c, msg)
        except:
            break

def main():
    threading.Thread(target=accept).start()

def isfirst():
    with open("/home/kral4/.check", "r") as f:
        content = f.read()
    if content.strip() == "True":
        return True
    else:
        return False
        
if __name__ == "__main__":
    main()
