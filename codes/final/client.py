import csv
import os
import socket
import threading
import time
import pygame

import Rsa
import Custom_Encryption

cords = [0, 0]


def recv():
    try:
        while 1:
            msg = c.recvfrom(1024)[0].decode()
            msg = Custom_Encryption.decrypt(msg, Custom_key)
            x, y = msg.split('.')
            cords[0] = int(x)
            cords[1] = int(y)
    except KeyboardInterrupt:
        return


# pre auth
serverAddressPort = ("127.0.0.1", 20003)
c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

pub, priv = Rsa.generate_keys()
c.sendto(f'rsa:{pub.n}${pub.e}'.encode(), serverAddressPort)

Custom_key = c.recvfrom(1024)[0]
Custom_key = Rsa.decrypt(Custom_key, priv)

# login and stuff

# game stuff
msg = Custom_Encryption.encrypt('connect', Custom_key)
c.sendto(msg.encode(), serverAddressPort)
pygame.init()
Screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
running = True
threading.Thread(target=recv, daemon=True).start()
oldX = 0
oldY = 0


def read_csv(filename):
    map = []
    with open(os.path.join(filename)) as data:
        data = csv.reader(data, delimiter=',')
        for row in data:
            map.append(list(row))
    return map  #


tiles_per_line = 18
tile_size = 64


def calcTopLeft(id: int):
    try:
        return id % tiles_per_line * tile_size, int(id / tiles_per_line) * tile_size
    except:
        return False


def tileDraw(xloc, yloc):
    x = 0
    y = 0
    for k in range(int(yloc / tile_size),
                   int(yloc / tile_size) + H + 2):  # cameraGroup.offset.y, cameraGroup.offset.y + 14
        for i in range(int(xloc / tile_size),
                       int(xloc / tile_size) + W + 1):  # cameraGroup.offset.x, cameraGroup.offset.x + 24
            try:
                if i >= 0 and k >= 0:
                    x2, y2 = (calcTopLeft(int(map[k][i])))
                    if int(map[k][i]) == 67:
                        print(k, i)

                    Screen.blit(tile_set, (x * tile_size - xloc % tile_size, y * tile_size - yloc % tile_size),
                                (int(x2), int(y2), tile_size, tile_size))
            except:
                pass
            x += 1
        y += 1
        x = 0


map = read_csv('GROUND1.csv')
tile_set = pygame.image.load('tileset64.png')
W, H = Screen.get_size()
width = W/2
height = H/2


W = int(W / tile_size)
H = int(H / tile_size)

playerimg = pygame.image.load("../../images/basics/alienBlue_stand.png")
playerimg = pygame.transform.scale(playerimg, (66, 92))
player_animation = [pygame.image.load("../../images/basics/BlueAlienBreakdance1.png"),
                    pygame.image.load("../../images/basics/BlueAlienBreakdance2.png"),
                    pygame.image.load("../../images/basics/BlueAlienBreakdance3.png"),
                    pygame.image.load("../../images/basics/BlueAlienBreakdance4.png")]
time_moved = 0
frame = 0
while running:
    frame += 1
    frame %= 4
    # Screen.fill('white')
    tileDraw(cords[0], cords[1])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    yDir = keys[pygame.K_s] - keys[pygame.K_w]
    xDir = keys[pygame.K_d] - keys[pygame.K_a]

    player_rect = playerimg.get_rect()
    player_rect.center = (width,height)

    if xDir or yDir:
        if time.time() - time_moved>0.001:
            cords[0]+=xDir
            cords[1]+=yDir
        Screen.blit(player_animation[int(frame%4)], player_rect)
    else:
        Screen.blit(playerimg, player_rect)

    if xDir != oldX or yDir != oldY:
        oldX = xDir
        oldY = yDir
        msg = f'move:{xDir}.{yDir}'
        msg = f'{len(msg)}${msg}'
        msg = 'commands:' + msg
        msg = Custom_Encryption.encrypt(msg, Custom_key)

        c.sendto(msg.encode(), serverAddressPort)
    pygame.display.update()
msg = Custom_Encryption.encrypt('leave', Custom_key)
c.sendto(msg.encode(), serverAddressPort)

# c.close()
