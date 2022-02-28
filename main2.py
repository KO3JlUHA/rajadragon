import pygame
import sys
import math
import time
import random
import webbrowser
import pyautogui
import socket





class snowBall():
    def __init__(self):
        self.dmg = 1
        self.range = 60
        self.speed = 8
        self.cooldown = 0.25
        self.price = 10
        self.spritePAth = "snowball.png"
        self.color = (255, 255, 255)
        self.radius = 5
        self.isMelee = False

        self.H = 10
        self.W = 10


class axe():
    def __init__(self):
        self.dmg = 15
        self.range = 80
        self.speed = 0
        self.cooldown = 3
        self.price = 250
        self.color = (100, 100, 100)
        self.radius = 70
        self.isMelee = True
        self.spritePAth = "axe.png"
        self.H = 100
        self.W = 25


class bow():
    def __init__(self):
        self.H = 50
        self.W = 15

        self.dmg = 10
        self.range = 65
        self.speed = 12  # gun will be 18 speed
        self.cooldown = 1
        self.price = 100
        self.spritePAth = "arrow.png"
        # w
        self.color = (255, 0, 0)
        self.radius = 5
        self.isMelee = False


def CheckCollision(x, y, xlen, ylen, x2, y2, xlen2, ylen2):
    inrangex = (x > x2 and x < x2 + xlen2) or (x2 > x and x2 < x + xlen)
    inrangey = (y > y2 and y < y2 + ylen2) or (y2 > y and y2 < y + ylen)
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
        self.isTyping = False
    def input(self):
        if (self.isTyping):
            return
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
    def __init__(self, mapX, mapY, width, height, health, speed, color):
        self.mapX = mapX
        self.mapY = mapY
        self.homeX = mapX
        self.homeY = mapY
        self.width = width
        self.height = height
        self.color = color
        self.isAlive = True
        self.health = health
        self.maxHealth = health
        self.deathTime = 0
        self.speed = speed
        self.timeOutOfRAnge = 0

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
    def __init__(self, x, y, mouseX, mouseY, weaponGiven):
        self.x = x
        self.y = y
        self.speed = weaponGiven.speed
        if (self.speed == 0):
            self.x = CameraGroup.half_w
            self.y = CameraGroup.half_h
        self.degree = 0
        self.path = weaponGiven.spritePAth
        self.weapon = weaponGiven
        self.damage = weaponGiven.dmg
        self.cooldown = weaponGiven.cooldown
        self.price = weaponGiven.price
        self.rangeToTravel = weaponGiven.range
        # self.color = weaponGiven.color
        self.radius = weaponGiven.radius
        self.mouseX = mouseX
        self.mouseY = mouseY
        self.hasToExist = True
        self.angle = math.atan2(y - mouseY, x - mouseX)
        self.velocityX = math.cos(self.angle) * self.speed
        self.velocityY = math.sin(self.angle) * self.speed

        self.H = weaponGiven.H
        self.W = weaponGiven.W

    def main(self, display, directionX, directionY):
        self.x -= int(self.velocityX + directionX)
        self.y -= int(self.velocityY + directionY)
        self.rangeToTravel -= 1
        self.hasToExist = self.rangeToTravel != 0
        images = pygame.image.load(self.path)
        if (self.speed == 0):
            if ((80 - self.rangeToTravel) % 5 == 0):
                # time.sleep(1)
                self.degree += 45
                self.x = CameraGroup.half_w
                self.y = CameraGroup.half_h
            images = pygame.transform.rotate(images, (self.degree))
            rect = images.get_rect(center=(CameraGroup.half_w, CameraGroup.half_h))
        else:
            images = pygame.transform.rotate(images, self.angle * -180 / math.pi)
            rect = images.get_rect(topleft = (self.x,self.y))
        Screen.blit(images, (rect))
        #return rect will be needed for colidion

        # pygame.draw.circle(display, self.color, (self.x, self.y), self.radius, self.out)


pygame.init()
Screen = pygame.display.set_mode((1280, 720))
Clock = pygame.time.Clock()

CameraGroup = CameraGroup()
player = Player((640, 320), CameraGroup)

mob = Mob(100, 200, 20, 50, 10, 5, (255, 0, 0))
mob2 = Mob(220, 101, 60, 120, 20, 5, (0, 255, 0))
moblist = [mob, mob2]
playerParticles = []
arrow = bow()
ball = snowBall()
sur = axe()
weapon_s = []
weapon_s.append(arrow)
weapon_s.append(ball)
weapon_s.append(sur)
weapon_used = weapon_s[0]
last_attack = 0

msg = ""




client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.43.40',80))

while True:
    data = client.recv(1024)
    if (data.decode()=='!RR'):
        pyautogui.press('volumeup', presses=100)
        webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    if CameraGroup.offset.x == 0 and CameraGroup.offset.y == 0:
        pygame.draw.rect(Screen, (255, 0, 0), (0, 0, 500, 500))
    mouseX, mouseY = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:  # weapon choice ↓
            if event.key == pygame.K_RETURN:
                player.isTyping = not player.isTyping
                if not player.isTyping:
                    msg = msg[1:]
                    while (msg.startswith("'")or msg.startswith("\\")):
                        msg = msg[1:]
                    # print(msg)
                    client.send(msg.encode())
                    msg = ""
            if not player.isTyping:
                if event.key == pygame.K_1:
                    weapon_used = weapon_s[0]
                elif event.key == pygame.K_2 and len(weapon_s) > 1:
                    weapon_used = weapon_s[1]
                elif event.key == pygame.K_3 and len(weapon_s) > 2:
                    weapon_used = weapon_s[2]  # weapon choice   ↑
        if not player.isTyping:
            if event.type == pygame.MOUSEBUTTONDOWN:  # attack ↓
                if event.button == 1 and time.time() > last_attack + weapon_used.cooldown:
                    playerParticles.append(
                        PlayerParticle(CameraGroup.half_w, CameraGroup.half_h, mouseX, mouseY, weapon_used))
                    last_attack = time.time()
        else:
            player.direction.x = 0
            player.direction.y = 0
            if event.type == pygame.KEYDOWN:
                try:
                    if event.key == 68 and len(msg) > 0:
                        msg = msg[:-1]
                    else:
                        pressed = chr(event.key)
                        keys = pygame.key.get_pressed()
                        if (keys[pygame.K_LSHIFT]):
                            if (pressed<='z' and pressed>='a'):
                                pressed = chr(event.key-32)
                            elif pressed=='0':
                                pressed=')'
                            elif pressed=='1':
                                pressed='!'
                            elif pressed=='2':
                                pressed='@'
                            elif pressed == '3':
                                pressed='#'
                            elif pressed == '4':
                                pressed='$'
                            elif pressed == '5':
                                pressed='%'
                            elif pressed == '6':
                                pressed='^'
                            elif pressed == '7':
                                pressed='&'
                            elif pressed == '8':
                                pressed='*'
                            elif pressed == '9':
                                pressed='('
                            elif pressed == '-':
                                pressed = '_'
                            elif pressed=='=':
                                pressed='+'
                            elif pressed== ';':
                                pressed=':'
                            elif pressed=="'":
                                pressed = '"'
                            elif pressed=="/":
                                pressed="?"
                            elif pressed==',':
                                pressed='<'
                            elif pressed=='.':
                                pressed='>'
                        if len(msg) <= 100:
                            msg += pressed
                except:
                    print('unsuported synbol')
                # attack   ↑
            # elif event.button == 3:
            #     playerParticles = playerParticles[1:]

    Screen.fill('#71ddee')
    CameraGroup.update()
    CameraGroup.CustomDraw(player)

    for mobi in moblist:
        if (
                mobi.mapX - 500 > mobi.homeX or mobi.mapX + 500 < mobi.homeX or mobi.mapY - 500 > mobi.homeY or mobi.mapY + 500 < mobi.homeY) and mobi.timeOutOfRAnge == 0:
            mobi.timeOutOfRAnge = time.time()
        if time.time() >= mobi.timeOutOfRAnge + 2 and mobi.timeOutOfRAnge != 0:
            mobi.mapX = mobi.homeX
            mobi.mapY = mobi.homeY
            mobi.timeOutOfRAnge = 0
        if mobi.deathTime + 10 <= time.time() or mobi.isAlive:
            if not mobi.isAlive:
                mobi.health = mobi.maxHealth
            mobi.isAlive = True
            if (CheckCollision(mobi.mapX - 200, mobi.mapY - 200, mobi.width + 400, mobi.height + 400,
                               player.rect.centerx - Borders.playerW / 2, player.rect.centery - Borders.playerH / 2,
                               Borders.playerW, Borders.playerH, )):
                x = random.randint(0, 1)
                if (x == 0):
                    if (mobi.mapX > player.rect.centerx - Borders.playerW / 2):
                        mobi.mapX -= mobi.speed
                    else:
                        mobi.mapX += mobi.speed
                else:
                    if (mobi.mapY > player.rect.centery - Borders.playerH / 2):
                        mobi.mapY -= mobi.speed
                    else:
                        mobi.mapY += mobi.speed
            mobi.main(Screen)
    for particle in playerParticles:
        flag = True
        for mobi in moblist:
            if mobi.isAlive and CheckCollision(mobi.mapX, mobi.mapY, mobi.width, mobi.height,
                                               particle.x - particle.radius + CameraGroup.offset.x,
                                               particle.y - particle.radius + CameraGroup.offset.y, particle.radius * 2,
                                               particle.radius * 2):
                flag = False
                mobi.health -= particle.damage
                if (mobi.isAlive and mobi.health <= 0):
                    mobi.isAlive = False
                    mobi.mapX = mobi.homeX
                    mobi.mapY = mobi.homeY
                    mobi.deathTime = time.time()
        if particle.hasToExist and (flag or weapon_used.isMelee):
            particle.main(Screen, player.direction.x * player.speed, player.direction.y * player.speed)
        else:
            playerParticles.remove(particle)
    # if CheckCollision(player.rect.centerx-Borders.playerW/2, player.rect.centery-Borders.playerH/2,
    #                   Borders.playerW, Borders.playerH, mob.mapX, mob.mapY, 120, 120):
    #     print("h")

    pygame.display.update()
    Clock.tick(60)
