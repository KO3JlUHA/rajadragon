import socket
import pygame


localIP = "0.0.0.0"
localPort = 20001
bufferSize = 1024


# Create a datagram socket
UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")
chat_shit = ''
chat_shit_ip = ''
# Listen for incoming datagrams
addresses=[]
cords=[]
UDPServerSocket.settimeout(0.1)
while 1:
#------------------------------------------------ cleaning the cords from left users
    for cord in cords:
        if cord=='!L':
            cords.remove(cord)
#-------------------------------------------------

#-------------------------------------------------  setting up pre needed data
    bytesAddressPair=''
    flug = False
    chat_flag = False
#-------------------------------------------------
#------------------------------------------------- checking for input
    try:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    except:
        pass
#-------------------------------------------------


#------------------------------------------------- if there were input check what were it
    if (len(bytesAddressPair)>0):
        message = bytesAddressPair[0].decode()
        address = bytesAddressPair[1]
        # -------------------------------------------------
        if (message.startswith('!hi')):
            addresses.append(address)
            message = message[3:]
            try:
                message=message.replace('(','')
                message=message.replace(')','')
                message=message.replace(' ','')
                message=message.replace(',','.')
            except:
                pass
            cords.append(message)
            flug=True
        elif message=='!':
            break
        elif message=='!L':
            cords[addresses.index(address)]=message
            addresses.remove(address)
        elif message.startswith('!CHAT'):
            chat_flag = True
            chat_shit=message
            chat_shit_ip = address
        elif message.startswith('!CORDS'):
            try:
                message = message[6:]
                #get the cords out of the message
                message=message.replace('(','')
                message=message.replace(')','')
                message=message.replace(' ','')
                message=message.replace(',','.')

                #TODO
                #create a rectangle for each recivne cord
                #check for mobs trigered
                #move the mobs if needed and break


                # player_rect = pygame.Rect(0, 0, 66, 92)
                # player_rect.center=(playercords)
                cords[addresses.index(address)]=message

            except:
                pass
#-------------------------------------------------
    if not chat_flag:
        for ip in addresses:
            tmp = cords[addresses.index(ip)]
            cords[addresses.index(ip)]= 'TEMP'
            print(cords)
            UDPServerSocket.sendto(str(cords).encode(),ip)
            cords[addresses.index(ip)] = tmp
    else:
        for ip in addresses:
            if ip != chat_shit_ip:
                UDPServerSocket.sendto(chat_shit.encode(),ip)
UDPServerSocket.close()