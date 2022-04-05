import time

import Rsa
import Custon_Encription
import socket

import colorama
from colorama import Fore

serverAddressPort = ("127.0.0.1", 20003)
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


pub, priv = Rsa.generate_keys()
UDPClientSocket.sendto(f'{pub.n}${pub.e}'.encode(), serverAddressPort)



key = UDPClientSocket.recvfrom(1024)[0]
print(Fore.RED + f'{key}')
key = Rsa.decrypt(key, priv)



#here comes the login






while 1:
    msg = input(Fore.WHITE + 'enter message: \n')
    msg = Custon_Encription.encript(key, msg)
    UDPClientSocket.sendto(msg.encode(), serverAddressPort)
    if msg == 'stop':
        break
