import threading
import socket
import Player

cords = [120, 120]

UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
localIP = "0.0.0.0"
localPort = 20003
UDPServerSocket.bind((localIP, localPort))

IPs = []  # list of ips
players = []  # list of objects Player.player()

changed = [False]

def HandleConectedClient():
    """
    recieves a packet from a client
    change the data acording to it
    accepts new users
    """
    msg, ip = UDPServerSocket.recvfrom(2048)
    changed[0] = True
    msg = msg.decode()
    if msg == '!HI':
        IPs.append(ip)
        players.append(Player.player(ip))
    elif msg == '!L':
        players.remove(players[IPs.index(ip)])
        IPs.remove(ip)
        UDPServerSocket.sendto('bye'.encode(), ip)
    else:
        pl = players[IPs.index(ip)]
        xDir, yDir = msg.split('.')
        xDir = int(xDir)
        yDir = int(yDir)
        pl.x += xDir
        pl.y += yDir


def sendInfo(ip):
    """
    sends a user all the info it needs

    the packets looks like:

    xCord.yCord

    """
    pl = players[IPs.index(ip)]
    # print('sending...')
    toSend = f'{pl.x}.{pl.y}'
    UDPServerSocket.sendto(toSend.encode(), ip)


def main():
    con = -1
    while 1:
        changed[0] = False
        if len(IPs) != con:
            print(f'Users COnected: {len(IPs)}')
            con = len(IPs)
        print(f'threads alive: {threading.active_count()-1}')
        for _ in range(len(IPs) + 2 - threading.active_count()):
            threading.Thread(target=HandleConectedClient).start()
            # tr2 = threading.Thread(target=sendInfo)
            # tr2.start()
        if changed[0]:
            for ip in IPs:
                sendInfo(ip)


if __name__ == '__main__':
    main()
