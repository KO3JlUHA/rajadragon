import pygame
import sys
import math
import socket
import Player as Basics

imgArrow = pygame.image.load('../../images/weapons/arrow.png')
imgSnowball = pygame.image.load('../../images/weapons/snowball.png')


class others():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("../../images/basics/alienBlue_stand.png")
        self.image = pygame.transform.scale(self.image, (66, 92))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def main(self):
        Screen.blit(self.image, self.rect)


def drawhealth(health):  # 100*300
    ycord = 720 - 50
    xcord = (1280 / 2) - 150
    healthrect = pygame.Rect((xcord, ycord), (health * 3, 30))
    pygame.draw.rect(Screen, (0, 255, 0), healthrect)
    xcord += health * 3
    healthrect = pygame.Rect((xcord, ycord), ((100 - health) * 3, 30))
    pygame.draw.rect(Screen, (255, 0, 0), healthrect)


bufferSize = 1024
serverAddressPort = ("127.0.0.1", 20003)
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPClientSocket.sendto('!HI'.encode(), serverAddressPort)

pygame.init()
Screen = pygame.display.set_mode((1280, 720))
Clock = pygame.time.Clock()
CameraGroup = Basics.CameraGroup()
player = Basics.Player((640, 320), CameraGroup)

particles = []
while True:
    Screen.fill('#71ddee')
    CameraGroup.update()
    CameraGroup.CustomDraw(player)

    othersList = []
    reciven = UDPClientSocket.recvfrom(bufferSize)[0].decode()
    for command in reciven.split('$'):
        if command.startswith('!LOC'):
            _, X, Y = command.split('|')
            X = int(X)
            Y = int(Y)
            player.center = (X, Y)
        elif command.startswith('!OTHER_p'):
            command = command[9:]
            if command:
                for dude in command.split('@'):
                    if dude:
                        X, Y = dude.split('|')
                        X = int(X) - CameraGroup.offset.x
                        Y = int(Y) - CameraGroup.offset.y
                        others(X, Y).main()
        elif command.startswith('!PARTICLES'):
            command = command[11:]
            if command:
                for particle in command.split('@'):
                    if particle:
                        X, Y, ANGLE, name = particle.split('|')
                        X = int(X)
                        Y = int(Y)
                        ANGLE = float(ANGLE)
                        ANGLE *= -180 / math.pi
                        img = ''
                        if name == 'bow':
                            img = imgArrow
                        elif name == 'snowball':
                            img = imgSnowball
                        img = pygame.transform.rotate(img, ANGLE)
                        Screen.blit(img, (X - CameraGroup.offset.x, Y - CameraGroup.offset.y))
        elif command.startswith('!HEALTH'):
            hlth = int(command.split('|')[-1])
            if hlth <= 0:
                UDPClientSocket.sendto('!L'.encode(), serverAddressPort)
                pygame.quit()
                sys.exit()
            drawhealth(hlth)

    mouseX, mouseY = pygame.mouse.get_pos()
    mouseXmap = int(mouseX + CameraGroup.offset.x)
    mouseYmap = int(mouseY + CameraGroup.offset.y)
    dirX, dirY = player.move()
    tosend = '!MOVE.' + str(dirX) + '.' + str(dirY)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            UDPClientSocket.sendto('!L'.encode(), serverAddressPort)
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            tosend += f'$!ATTACK.{mouseXmap}.{mouseYmap}'
    for particle in particles:
        particle.main(Screen)
    print(tosend)
    UDPClientSocket.sendto(tosend.encode(), serverAddressPort)

    pygame.display.update()
    Clock.tick(60)
