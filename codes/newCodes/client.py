import pygame
import sys
import math
import socket
import Player as Basics

imgArrow = pygame.image.load('../../images/weapons/arrow.png')
imgSnowball = pygame.image.load('../../images/weapons/snowball.png')
iconBow = pygame.image.load('../../images/icons/icon-bow.png')
iconCumball = pygame.image.load('../../images/icons/icon-cumball.png')


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
    ycord = Basics.Sizes.ScreenH - 50
    xcord = (Basics.Sizes.ScreenW / 2) - 150
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
fontlvl = pygame.font.Font("freesansbold.ttf", 20)
# Screen = pygame.display.set_mode((Basics.Sizes.ScreenW, Basics.Sizes.ScreenH))
Screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
Basics.Sizes.ScreenW, Basics.Sizes.ScreenH = Screen.get_size()

Clock = pygame.time.Clock()
CameraGroup = Basics.CameraGroup()
player = Basics.Player((640, 320), CameraGroup)
picked = 0
inventory = ['', '', '', '', '', 'FUCK']
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
        elif command.startswith('!PICKED'):
            picked = int(command.split('|')[-1])
        elif command.startswith('!INV|'):
            command = command[5:]
            itemI = 0
            for item in command.split('@')[0:6]:
                inventory[itemI] = item
                itemI += 1
    # pygame.draw.rect(Screen, (255, 0, 0), player.rect, 4)
    mouseX, mouseY = pygame.mouse.get_pos()
    mouseXmap = int(mouseX + CameraGroup.offset.x)
    mouseYmap = int(mouseY + CameraGroup.offset.y)
    dirX, dirY = player.move()
    tosend = '!MOVE.' + str(dirX) + '.' + str(dirY)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            UDPClientSocket.sendto('!L'.encode(), serverAddressPort)
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            tosend += f'$!ATTACK.{mouseXmap}.{mouseYmap}'
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                tosend += '$!PICK.0'
            elif event.key == pygame.K_2:
                tosend += '$!PICK.1'
            elif event.key == pygame.K_3:
                tosend += '$!PICK.2'
            elif event.key == pygame.K_4:
                tosend += '$!PICK.3'
            elif event.key == pygame.K_5:
                tosend += '$!PICK.4'
            elif event.key == pygame.K_6:
                tosend += '$!PICK.5'
    UDPClientSocket.sendto(tosend.encode(), serverAddressPort)

    rectt = pygame.Rect((1000, 900), (90, 90))
    rectt.bottomright = (Basics.Sizes.ScreenW, Basics.Sizes.ScreenH)
    for i in range(6):
        pygame.draw.rect(Screen, (100, 100, 100), rectt, 10)

        if inventory[5 - i]:
            rectt.bottom += 10
            rectt.right += 10
            lvl, name = inventory[5 - i].split('|')
            toShow = fontlvl.render(lvl, True, (0, 0, 100))
            icon = iconBow
            if name == 'snowball':
                icon = iconCumball
            Screen.blit(icon, rectt)
            # toShow = fontlvl.render(str(weapons_list[5 - i].lvl), True, (0, 0, 100))
            Screen.blit(toShow, rectt)
            rectt.bottom -= 10
            rectt.right -= 10
        rectt.right -= 80
    for i in range(picked + 1):
        rectt.right += 80
    pygame.draw.rect(Screen, (255, 255, 255), rectt, 10)
    pygame.display.update()
    Clock.tick(60)
