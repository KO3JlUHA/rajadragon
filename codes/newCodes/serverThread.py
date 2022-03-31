import queue
import threading
import socket
import time

UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
localIP = "0.0.0.0"
localPort = 20003
UDPServerSocket.bind((localIP, localPort))


q = queue.Queue()
q2 = queue.Queue()
def recv(tp):
    time.sleep(1)
    print(tp)

def qu():
    quitF.append(input('press enter to quit'))

t = time.time()
quitF = []
toPrint = ['a','b','c','d','e']
while not quitF:
    treads = []
    for p in toPrint:
        tr = threading.Thread(target=recv,args =(p))
        treads.append(tr)
        tr.start()
    qui = threading.Thread(target=qu)
    qui.start()
    qui.join()
    for tr in treads:
        tr.join()
print(time.time()-t)