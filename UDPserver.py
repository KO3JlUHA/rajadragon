import socket

localIP = "0.0.0.0"

localPort = 20001

bufferSize = 1024

msgFromServer = "Hello UDP Client"

bytesToSend = str.encode(msgFromServer)

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams
addresses=[]
while (True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0].decode()
    try:
        message=message.replace('(','')
        message=message.replace(')','')
        message=message.replace(' ','')
    except:
        pass
    address = bytesAddressPair[1]
    if (address not in addresses):
        addresses.append(address)
    if (message=='!'):
        break
    if (message):
        print(message)
    for ip in addresses:
        if ip!=address:
            UDPServerSocket.sendto(message.encode(),ip)
        else:
            UDPServerSocket.sendto("".encode(),ip)

UDPServerSocket.close()
