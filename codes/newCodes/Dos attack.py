import threading
import socket
import time

serverAddressPort = ("127.0.0.1", 20003)
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
def s():
    pass

def main():

    while 1:
        msg = input('enter cords like x|y')
        UDPClientSocket.sendto(msg.encode(), serverAddressPort)

    pass


if __name__ == '__main__':
    main()


