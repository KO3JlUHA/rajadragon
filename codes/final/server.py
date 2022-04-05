import socket
import threading
import Rsa
import Custom_Encryption
import player
import time
from typing import List

ips = []
keys = []

players_in_game: List[player.Player] = []
ips_in_game = []


def recv():
    while 1:
        Data, ip = s.recvfrom(1024)
        Data = Data.decode()

        if Data.startswith('rsa:'):
            threading.Thread(target=recv).start()
            Data = Data[4:]
            n, e = Data.split('$')
            n = int(n)
            e = int(e)
            rsaKey = Rsa.rsa.key.PublicKey(e=e, n=n)
            Custom_key = Custom_Encryption.genKey(5)
            ips.append(ip)
            keys.append(Custom_key)
            encriptedKey = Rsa.encrypt(Custom_key, rsaKey)
            s.sendto(encriptedKey, ip)
        else:
            Data = Custom_Encryption.decrypt(Data, keys[ips.index(ip)])
            if Data == 'connect':
                players_in_game.append(player.Player())
                ips_in_game.append(ip)
            elif Data == 'leave':
                players_in_game.remove(players_in_game[ips_in_game.index(ip)])
                ips_in_game.remove(ip)
                keys.remove(keys[ips.index(ip)])
                ips.remove(ip)
                return
            elif Data.startswith('commands:'):
                Data = Data[9:]
                while Data:
                    lenOfCommand = Data.split('$')[0]
                    lenOfCommandWithoutLen = len(lenOfCommand) + 1
                    lenOfCommand = int(lenOfCommand)
                    command = Data[lenOfCommandWithoutLen:lenOfCommandWithoutLen + lenOfCommand]
                    Data = Data[lenOfCommand + lenOfCommandWithoutLen:]

                    if command.startswith('move:'):
                        command = command[5:]
                        x, y = command.split('.')
                        players_in_game[ips_in_game.index(ip)].dirX = int(x)
                        players_in_game[ips_in_game.index(ip)].dirY = int(y)


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
localIP = "0.0.0.0"
localPort = 20003
s.bind((localIP, localPort))


def main():
    threading.Thread(target=recv).start()
    while 1:
        for i, ip in enumerate(ips_in_game):
            print(i)
            if time.time() - players_in_game[i].timeMoved > 0.001:
                print('time passed')
                players_in_game[i].timeMoved = time.time()
                players_in_game[i].x += players_in_game[i].dirX
                players_in_game[i].y += players_in_game[i].dirY
                msg = f'{players_in_game[i].x}.{players_in_game[i].y}'
                msg = Custom_Encryption.encrypt(msg, keys[ips.index(ip)])
                s.sendto(msg.encode(), ip)


if __name__ == '__main__':
    main()
