import Rsa
import Custon_Encription
import socket

import colorama
from colorama import Fore

UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
localIP = "0.0.0.0"
localPort = 20003
UDPServerSocket.bind((localIP, localPort))

keyss, ip = UDPServerSocket.recvfrom(1024)
keyss = keyss.decode()
print(Fore.RED + keyss)
n, e = keyss.split('$')
n = int(n)
e = int(e)

key2 = Rsa.rsa.key.PublicKey(e=e, n=n)

key = Custon_Encription.genKey(5)

ciphertext = Rsa.encrypt(key, key2)

UDPServerSocket.sendto(ciphertext, ip)

msg = UDPServerSocket.recvfrom(1024)[0].decode()

print(msg)

msg = Custon_Encription.decript(key, msg)

print(Fore.GREEN + msg)

