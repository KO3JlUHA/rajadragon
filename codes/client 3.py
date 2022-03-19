import pygame
import sys
import math
import socket


class others():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("../images/basics/alienBlue_stand.png")
        self.image = pygame.transform.scale(self.image, (66, 92))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def main(self):
        Screen.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)
        self.position = position
        self.image = pygame.image.load('../images/basics/alienBlue_stand.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (66, 92))
        self.rect = self.image.get_rect(center=position)
        self.center = (0, 0)

    def update(self):
        self.rect.center = self.center


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()

        self.offset = pygame.math.Vector2()
        self.half_w = self.displaySurface.get_size()[0] // 2
        self.half_h = self.displaySurface.get_size()[1] // 2

        self.groundSurf = pygame.image.load('../images/basics/ground2.jpg').convert_alpha()
        self.groundRect = self.groundSurf.get_rect(topleft=(0, 0))

    def centerTargetCamera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def CustomDraw(self, player):
        self.centerTargetCamera(player)

        groundOffset = self.groundRect.topleft - self.offset
        self.displaySurface.blit(self.groundSurf, groundOffset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image, offset_pos)


class PlayerParticle:
    def __init__(self, x, y, mouseX, mouseY):
        self.x = x
        self.y = y
        self.mouseX = mouseX
        self.mouseY = mouseY
        self.speed = 15
        self.angle = math.atan2(y - mouseY, x - mouseX)
        self.velocityX = math.cos(self.angle) * self.speed
        self.velocityY = math.sin(self.angle) * self.speed

    def main(self, display):
        self.x -= int(self.velocityX)
        self.y -= int(self.velocityY)
        pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), 5)


bufferSize = 1024
serverAddressPort = ("127.0.0.1", 20003)
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPClientSocket.sendto('!HI'.encode(), serverAddressPort)

pygame.init()
Screen = pygame.display.set_mode((1280, 720))
Clock = pygame.time.Clock()
CameraGroup = CameraGroup()
player = Player((640, 320), CameraGroup)

while True:
    othersList = []
    reciven = UDPClientSocket.recvfrom(bufferSize)[0].decode()
    for command in reciven.split('$'):
        if command.startswith('!LOC'):
            _, X, Y = command.split('.')
            X = int(X)
            Y = int(Y)
            player.center = (X, Y)
        elif command.startswith('!OTHER_p'):
            command = command[9:]
            if command:
                for dude in command.split('@'):
                    if dude:
                        X, Y = dude.split('.')
                        X = int(X) - CameraGroup.offset.x
                        Y = int(Y) - CameraGroup.offset.y
                        othersList.append(others(X, Y))

    Screen.fill('#71ddee')
    CameraGroup.update()
    CameraGroup.CustomDraw(player)

    for other in othersList:
        other.main()

    mouseX, mouseY = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            UDPClientSocket.sendto('!L'.encode(), serverAddressPort)
            pygame.quit()
            sys.exit()

    dirX = 0
    dirY = 0
    if keys[pygame.K_w]:
        dirY -= 1

    if keys[pygame.K_s]:
        dirY += 1

    if keys[pygame.K_d]:
        dirX += 1

    if keys[pygame.K_a]:
        dirX -= 1

    tosend = '!MOVE.' + str(dirX) + '.' + str(dirY)
    UDPClientSocket.sendto(tosend.encode(), serverAddressPort)

    pygame.display.update()
    Clock.tick(60)
