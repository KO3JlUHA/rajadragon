import sys

import pygame
import socket

serverAddressPort = ("127.0.0.1", 20003)
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPClientSocket.sendto('!HI'.encode(), serverAddressPort)

pygame.init()
Screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


def move():
    keys = pygame.key.get_pressed()
    return int(keys[pygame.K_d] - keys[pygame.K_a]), int(keys[pygame.K_s] - keys[pygame.K_w])

running = True
while running:
    Screen.fill('#71ddee')
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            UDPClientSocket.sendto('!L'.encode(), serverAddressPort)
            pygame.quit()
            running = False
            sys.exit()
    msg = UDPClientSocket.recvfrom(2048)[0].decode()
    x, y = msg.split('.')
    pygame.draw.rect(Screen, (255, 0, 0), ((int(x), int(y)), (100, 100)))
    dirX, dirY = move()
    if dirY or dirX:
        UDPClientSocket.sendto(f'{dirX}.{dirY}'.encode(), serverAddressPort)
    pygame.display.update()
