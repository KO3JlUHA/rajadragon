import pygame
import sys
import math


def CheckCollision(x, y, xlen, ylen, x2, y2, xlen2, ylen2):
    inrangex= (x>x2 and x<x2+xlen2) or (x2>x and x2<x+xlen)
    inrangey = (y>y2 and y<y2+ylen2) or (y2>y and y2<y+ylen)
    return inrangex and inrangey


class Borders():
    playerH = 92
    playerW = 66
    screenH = 1300
    screenW = 1950
    blockX = 60
    blockY = 60



class Player(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)
        self.health = 100
        self.position = position
        self.image = pygame.image.load('alienBlue_stand.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (Borders.playerW, Borders.playerH))
        self.rect = self.image.get_rect(center=position)
        self.direction = pygame.math.Vector2()
        self.speed = 6

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and (CameraGroup.offset.y + CameraGroup.half_h) > Borders.playerH / 2:
            self.direction.y = -1
        elif keys[pygame.K_s] and (CameraGroup.offset.y + CameraGroup.half_h) < Borders.screenH - Borders.playerH / 2:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d] and (CameraGroup.offset.x + CameraGroup.half_w) < Borders.screenW - Borders.playerW / 2:
            self.direction.x = 1
        elif keys[pygame.K_a] and (CameraGroup.offset.x + CameraGroup.half_w) > Borders.playerW / 2:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed


class Mob():
    def __init__(self, mapX, mapY, width, color):
        self.mapX = mapX
        self.mapY = mapY
        self.width = width
        self.height = 120
        self.color = color
        self.health = 100

    def main(self, display):
        pygame.draw.rect(display, self.color,
                         (self.mapX - CameraGroup.offset.x, self.mapY - CameraGroup.offset.y, self.width, self.height))


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()

        self.offset = pygame.math.Vector2()
        self.half_w = self.displaySurface.get_size()[0] // 2
        self.half_h = self.displaySurface.get_size()[1] // 2

        self.groundSurf = pygame.image.load('ground2.jpg').convert_alpha()
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
    def __init__(self, x, y, mouseX, mouseY, range, damage):
        self.x = x
        self.y = y
        self.damage = damage
        self.mouseX = mouseX
        self.mouseY = mouseY
        self.speed = 15
        self.rangeToTravel = range
        self.hasToExist = True
        self.angle = math.atan2(y - mouseY, x - mouseX)
        self.velocityX = math.cos(self.angle) * self.speed
        self.velocityY = math.sin(self.angle) * self.speed

    def main(self, display, directionX, directionY):
        self.x -= int(self.velocityX + directionX)
        self.y -= int(self.velocityY + directionY)
        self.rangeToTravel -= 1
        self.hasToExist = self.rangeToTravel != 0
        pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), 5)


pygame.init()
Screen = pygame.display.set_mode((1280, 720))
Clock = pygame.time.Clock()

CameraGroup = CameraGroup()
player = Player((640, 320), CameraGroup)
mob = Mob(100, 200, 120, (255, 0, 0))
mob2 = Mob(220, 101, 10, (0, 255, 0))
moblist = [mob,mob2]
playerParticles = []
while True:
    if CameraGroup.offset.x == 0 and CameraGroup.offset.y == 0:
        pygame.draw.rect(Screen, (255, 0, 0), (0, 0, 500, 500))
    mouseX, mouseY = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                playerParticles.append(PlayerParticle(CameraGroup.half_w, CameraGroup.half_h, mouseX, mouseY, 30, 21))
            elif event.button == 3:
                playerParticles = playerParticles[1:]

    Screen.fill('#71ddee')
    CameraGroup.update()
    CameraGroup.CustomDraw(player)


    for mobi in moblist:
        mobi.main(Screen)
    for particle in playerParticles:
        flag = True
        for mobi in moblist:
            if CheckCollision(mobi.mapX, mobi.mapY, mobi.width, mobi.height, particle.x+CameraGroup.offset.x, particle.y+CameraGroup.offset.y, 10,10):
                flag = False
                mobi.health-=particle.damage
                if (mobi.health<=0):
                    moblist.remove(mobi)
        if particle.hasToExist and flag:
            particle.main(Screen, player.direction.x * player.speed, player.direction.y * player.speed)
        else:
            playerParticles.remove(particle)
    if CheckCollision(player.rect.centerx-Borders.playerW/2, player.rect.centery-Borders.playerH/2,
                      Borders.playerW, Borders.playerH, mob.mapX, mob.mapY, 120, 120):
        print("h")

    pygame.display.update()
    Clock.tick(60)
