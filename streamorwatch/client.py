import socket
import time
import zlib
import cv2
import pyautogui
import sys
import os


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("3.65.21.124", 54746))


def ping(s):
    ping2server = 0
    start = time.time()
    s.sendall("PING".encode())
    if s.recv(4096).decode().strip() == "PONG":
        ping2server = time.time() - start 
        print("Ping :", ping2server)
    else:
        print("Something went wrong")
    del start
    del ping2server

def watcher(s):
    s.sendall("WATCHER".encode())
    status = s.recv(4096).decode().strip()
    if status == "WELCOME":
        while True:
            try:
                lenghtofdata = s.recv(4096).decode().strip()
                lenghtofdata = int(lenghtofdata)
                data = b""
                while True:
                    if len(data) >= lenghtofdata:
                        break
                    else:
                        newdata = s.recv(4096)
                        data += newdata
                with open("saved.png", "wb") as f:
                    f.write(zlib.decompress(data))
                wind = cv2.namedWindow("test", cv2.WINDOW_NORMAL)
                img = cv2.imread("saved.png")
                cv2.imshow(wind, img)
                cv2.waitKey(30)
            except UnicodeDecodeError:
                pass
            except ConnectionResetError:
                sys.exit(0)
                break
    elif status == "NO_STREAM":
        print("No stream right now try again later")
    else:
        print(status)

def streamer(s):
    s.sendall("STREAMER".encode())
    def ss(c):
        while True:
            pyautogui.screenshot("a.png")
            with open("a.png", "rb") as f:
                data = f.read()
            data2send = zlib.compress(data, 9)
            try:
                c.sendall(str(len(data2send)).encode())
                c.sendall(data2send)
            except ConnectionResetError:
                sys.exit(0)
                break
    status = s.recv(4096).decode().strip()
    if status == "WELCOME":
        ss(s,)
    else:
        print(status)

def main(s):
    while True:
        aswho = input("->")
        if aswho == "watcher":
            watcher(s,)
            break
        elif aswho == "streamer":
            streamer(s,)
            break
        elif aswho == "ping":
            ping(s,)
main(s,)