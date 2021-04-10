import socket
import multiprocessing
import datetime
import atexit
import time
threads = []

def killthreads():
    global threads
    for t in threads:
        t.terminate()

def log(data2log):
    with open("logs.txt", "a") as f:
        f.write(str(datetime.datetime.now()) + " | " + str(data2log) + "\n")

def listen(ip, port, send_message, message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, port))
    s.listen()
    while True:
        c, addr = s.accept()
        log("Connection accepted from " + str(addr) + " Port:" +str(port))
        if send_message == 1:
            try:
                c.sendall(message.encode())
                log("Message sent to" + str(addr) + " Port:" +str(port))
                data = c.recv(4096)
                log(f"Data - {str(data)} - received from " + str(addr) + " Port:" +str(port))
            except:
                pass
            try:
                c.shutdown(socket.SHUT_RDWR)
                c.close()
            except:
                pass
            log("Connection closed to " + str(addr) + " Port:" +str(port))
        else:
            try:
                data = c.recv(4096)
                log(f"Data - {str(data)} - received from " + str(addr) + " Port:" +str(port))
                c.shutdown(socket.SHUT_RDWR)
                c.close()
            except:
                pass
            log("Connection closed to " + str(addr) + " Port:" +str(port))


def main():
    global threads
    ip = "0.0.0.0"
    send_message = 0
    message = "Blocked"
    port_range = "3000,3500"
    port_range = port_range.split(",")
    for port in range(int(port_range[0]), int(port_range[1])):
        p = multiprocessing.Process(target=listen, args=(ip, port, send_message, message))
        p.start()
        threads.append(p)
    print("Done. Waiting for bears \n{} Threads Running".format(len(threads)))
    log("Done. Waiting for bears, {} Threads Running".format(len(threads)))

if __name__ == "__main__":
    atexit.register(killthreads)
    main()
