import pygame
import sys
import math
import time
import random
import webbrowser
import pyautogui
import socket

bufferSize = 1024
serverAddressPort = ("127.0.0.1", 20001)


class snowBall():
    def __init__(self, lvl):
        self.lvl = lvl
        self.dmg = self.lvl  # == lvl
        self.range = 60
        self.speed = 8
        self.cooldown = 0.25
        self.price = 10 * self.lvl
        self.upgradeCost = self.lvl * 15
        self.image = pygame.image.load("snowball.png")
        self.isMelee = False

    def __repr__(self):
        return ("snowball lvl " + str(self.lvl))

    def upgrate(self):
        if (player.gold >= self.upgradeCost):
            player.gold -= self.upgradeCost
            self.lvl += 1
            self.price = self.lvl * 10
            self.upgradeCost = self.lvl * 15
            self.dmg = self.lvl


class axe():
    def __init__(self, lvl):
        self.lvl = lvl
        self.dmg = self.lvl / 4
        self.range = 80
        self.speed = 0
        self.cooldown = 3
        self.price = self.lvl * 250
        self.upgradeCost = lvl * 300
        self.isMelee = True
        self.image = pygame.image.load("axe.png")

    def __repr__(self):
        return ("axe lvl " + str(self.lvl))

    def upgrate(self):
        if (player.gold >= self.upgradeCost):
            player.gold -= self.upgradeCost
            self.lvl += 1
            self.price = self.lvl * 250
            self.upgradeCost = self.lvl * 300
            self.dmg = self.lvl / 4


class bow():
    def __init__(self, lvl):
        self.lvl = lvl
        self.dmg = self.lvl * 4  # =lvl*4
        self.range = 60
        self.speed = 12  # gun will be 18 speed
        self.cooldown = 1
        self.price = self.lvl * 70
        self.upgradeCost = lvl * 100
        self.image = pygame.image.load("arrow.png")
        self.isMelee = False

    def __repr__(self):
        return ("bow lvl " + str(self.lvl))

    def upgrate(self):
        if (player.gold >= self.upgradeCost):
            player.gold -= self.upgradeCost
            self.lvl += 1
            self.price = self.lvl * 70
            self.upgradeCost = self.lvl * 100
            self.dmg = self.lvl * 4


class spear():
    def __init__(self, x, y, aimx, aimy):
        self.x = x
        self.y = y
        self.aimx = aimx
        self.aimy = aimy
        self.dmg = 10
        self.range = 60
        self.speed = 8
        self.cooldown = 1.5
        self.path = "arrow.png"

        self.angle = math.atan2(y - aimy, x - aimx)
        self.velocityX = math.cos(self.angle) * self.speed
        self.velocityY = math.sin(self.angle) * self.speed
        self.image = pygame.image.load(self.path)
        self.rect = self.image.get_rect()
        self.image = pygame.transform.rotate(self.image, self.angle * -180 / math.pi)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def main(self, directionX, directionY):
        self.x -= int(self.velocityX + directionX)
        self.y -= int(self.velocityY + directionY)
        self.range -= 1
        if self.range == 0:
            return
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        Screen.blit(self.image, self.rect)
        # pygame.draw.rect(Screen,(255,0,0),self.rect,4)


class Borders():
    playerH = 92
    playerW = 66
    screenH = 1300
    screenW = 1950
    blockX = 60
    blockY = 60


class others():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = pygame.image.load("alienBlue_stand.png")
        self.image = pygame.transform.scale(self.image, (Borders.playerW, Borders.playerH))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def main(self):
        self.rect.center = (self.x, self.y)
        Screen.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)
        self.isTyping = False
        self.health = 100
        self.gold = 0
        self.position = position
        self.image = pygame.image.load('alienBlue_stand.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (Borders.playerW, Borders.playerH))
        self.rect = self.image.get_rect(center=position)
        self.direction = pygame.math.Vector2()
        self.speed = 6

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
    def __init__(self, mapX, mapY, health, speed, range, travelrange):
        self.x = mapX
        self.y = mapY
        self.range = range
        self.homeX = mapX
        self.homeY = mapY
        self.travelRange = travelrange
        self.worth = 150
        self.isAlive = True
        self.health = health
        self.maxHealth = health
        self.deathTime = 0
        self.speed = speed
        self.timeOutOfRAnge = 0
        self.last_attack = 0
        self.spears = []
        self.images = pygame.image.load('mob.png').convert_alpha()
        self.rect = self.images.get_rect(topleft=(self.x, self.y))
        self.rectHome = pygame.Rect((self.x - CameraGroup.offset.x, self.y - CameraGroup.offset.x),
                                    (self.travelRange, self.travelRange))
        self.rectHome.center = self.rect.center
        self.rectTriger = pygame.Rect((self.x, self.y),
                                      (self.rect.width + self.range * 2, self.rect.height + self.range * 2))
        self.rectTriger.center = self.rect.center

    def main(self):
        self.x -= CameraGroup.offset.x
        self.y -= CameraGroup.offset.y
        self.rect.topleft = (self.x, self.y)
        self.rectHome.center = (self.homeX - CameraGroup.offset.x, self.homeY - CameraGroup.offset.y)
        self.rectTriger.center = self.rect.center
        # pygame.draw.rect(Screen, (0, 0, 255), self.rectHome, 6)
        # pygame.draw.rect(Screen,(255,0,0),self.rectTriger,10)
        # pygame.draw.rect(Screen, (0, 255, 0), self.rect, 6)
        Screen.blit(self.images, (self.rect))
        self.x += CameraGroup.offset.x
        self.y += CameraGroup.offset.y


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
        self.damage = weaponGiven.dmg
        self.cooldown = weaponGiven.cooldown
        self.rangeToTravel = weaponGiven.range
        self.mouseX = mouseX
        self.mouseY = mouseY
        self.hasToExist = True
        self.angle = math.atan2(y - mouseY, x - mouseX)
        self.velocityX = math.cos(self.angle) * self.speed
        self.velocityY = math.sin(self.angle) * self.speed
        self.image = weaponGiven.image
        self.rect = self.image.get_rect()

    def main(self, display, directionX, directionY):
        self.x -= int(self.velocityX + directionX)
        self.y -= int(self.velocityY + directionY)
        self.rangeToTravel -= 1
        self.hasToExist = self.rangeToTravel != 0
        images = self.image
        if (self.speed == 0):
            if ((80 - self.rangeToTravel) % 5 == 0):
                self.degree += 45
                self.x = CameraGroup.half_w
                self.y = CameraGroup.half_h
            images = pygame.transform.rotate(images, (self.degree))
            self.rect = images.get_rect(center=(CameraGroup.half_w, CameraGroup.half_h))
        else:
            images = pygame.transform.rotate(images, self.angle * -180 / math.pi)
            self.rect = images.get_rect(topleft=(self.x, self.y))
        Screen.blit(images, (self.rect))


pygame.init()
Screen = pygame.display.set_mode((1280, 720))
Clock = pygame.time.Clock()

CameraGroup = CameraGroup()
player = Player((1000, 320), CameraGroup)
rectScreen = pygame.Rect((CameraGroup.offset.x, CameraGroup.offset.y), (1280, 720))

mob = Mob(100, 200, 10, 5, 400, 1000)
mob2 = Mob(220, 101, 20, 5, 400, 1000)
moblist = [mob, mob2]
xcord = 0
ycord = 0
playerParticles = []
mobParticles = []
arrow = bow(100)
ball = snowBall(100)
sur = axe(100)
weapon_s = []
weapon_s.append(arrow)
weapon_s.append(ball)
weapon_s.append(sur)
weapon_used = weapon_s[0]
last_attack = 0
prect = pygame.Rect((CameraGroup.half_w, CameraGroup.half_h), (Borders.playerW, Borders.playerH))
prect.center = (CameraGroup.half_w, CameraGroup.half_h)
rectScreen.center = prect.center

i = 0

msg = ''
quitflag = False


UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPClientSocket.sendto("!hi".encode(), serverAddressPort)
bytesToSend = str(player.rect.center).encode()
UDPClientSocket.sendto(bytesToSend, serverAddressPort)





while True:
    rectScreen.center = prect.center
    if player.health <= 0:
        quitflag = True
    inventory = [weapon_s, player.gold]
    if CameraGroup.offset.x == 0 and CameraGroup.offset.y == 0:
        pygame.draw.rect(Screen, (255, 0, 0), (0, 0, 500, 500))
    mouseX, mouseY = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or quitflag:
            UDPClientSocket.sendto('!L'.encode(), serverAddressPort)
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:  # weapon choice ↓
            if event.key == pygame.K_RETURN:
                player.isTyping = not player.isTyping
                if not player.isTyping:
                    msg = msg[1:]
                    while (msg.startswith("'") or msg.startswith("\\")):
                        msg = msg[1:]
                    if '!inventory'.startswith(msg) and len(msg) > 1:
                        msg = 'weapons: '
                        for i in range(len(inventory[0])):
                            msg += str(inventory[0][i])
                            msg += ', '
                        msg += 'gold: '
                        msg += str(inventory[1])
                    if ('!upgrate'.startswith(msg) and len(msg) > 1):
                        weapon_used.upgrate()
                        msg = 'new lvl is '
                        msg += str(weapon_used.lvl)
                    if ('!price'.startswith(msg) and len(msg) > 1):
                        msg = 'the upgrate price is: '
                        msg += str(weapon_used.upgradeCost)
                    print(msg)
                    UDPClientSocket.sendto(msg.encode(), serverAddressPort)
                    msg = ''
            if not player.isTyping:
                if event.key == pygame.K_TAB:
                    pyautogui.press('volumeup', presses=100)
                    webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
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
                        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                            if (pressed <= 'z' and pressed >= 'a'):
                                pressed = chr(event.key - 32)
                            elif pressed == '0':
                                pressed = ')'
                            elif pressed == '1':
                                pressed = '!'
                            elif pressed == '2':
                                pressed = '@'
                            elif pressed == '3':
                                pressed = '#'
                            elif pressed == '4':
                                pressed = '$'
                            elif pressed == '5':
                                pressed = '%'
                            elif pressed == '6':
                                pressed = '^'
                            elif pressed == '7':
                                pressed = '&'
                            elif pressed == '8':
                                pressed = '*'
                            elif pressed == '9':
                                pressed = '('
                            elif pressed == '-':
                                pressed = '_'
                            elif pressed == '=':
                                pressed = '+'
                            elif pressed == ';':
                                pressed = ':'
                            elif pressed == "'":
                                pressed = '"'
                            elif pressed == "/":
                                pressed = "?"
                            elif pressed == ',':
                                pressed = '<'
                            elif pressed == '.':
                                pressed = '>'
                        if len(msg) <= 100:
                            msg += pressed
                except:
                    x = 1

    Screen.fill('#71ddee')
    CameraGroup.update()
    CameraGroup.CustomDraw(player)

    otherPlayer = []
    if player.direction.x or player.direction.y or len(playerParticles)>0:
        bytesToSend = str(player.rect.center).encode()
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    reciven = UDPClientSocket.recvfrom(bufferSize)[0].decode()
    if reciven:
        reciven = reciven.replace('[','')
        reciven = reciven.replace(']','')
        reciven = reciven.replace("'",'')
        reciven = reciven.replace(' ','')

        #here we have cords like 1486,1094, 1798,674
        print(reciven)
        for Pcords in reciven.split(','):
            print(Pcords)
            if Pcords!='TEMP' and Pcords != '!L':
                (xcord, ycord) = Pcords.split('.')
                xcord = int(xcord)
                ycord = int(ycord)
                player2 = others()
                player2.x = xcord - CameraGroup.offset.x
                player2.y = ycord - CameraGroup.offset.y
                otherPlayer.append(player2)
        for players in otherPlayer:
            players.main()
    for mobi in moblist:
        if (not mobi.rect.colliderect(mobi.rectHome)) and mobi.timeOutOfRAnge == 0:
            mobi.timeOutOfRAnge = time.time()
        if time.time() >= mobi.timeOutOfRAnge + 2 and mobi.timeOutOfRAnge != 0:
            mobi.x = mobi.homeX
            mobi.y = mobi.homeY
            mobi.health = mobi.maxHealth
            mobi.timeOutOfRAnge = 0
        if mobi.deathTime + 10 <= time.time() or mobi.isAlive:  # respawn or still alive
            if not mobi.isAlive:
                mobi.health = mobi.maxHealth
                mobi.spears = []
                mobi.main()
            mobi.isAlive = True
            if (mobi.rectTriger.colliderect(prect) and mobi.isAlive and i != 0):
                if (mobi.last_attack + 1.5 < time.time()):
                    spr = spear(mobi.x - CameraGroup.offset.x, mobi.y - CameraGroup.offset.y, CameraGroup.half_w,
                                CameraGroup.half_h)
                    mobi.last_attack = time.time()
                    mobi.spears.append(spr)
                x = random.randint(0, 1)
                if (x == 0):
                    if (mobi.x > player.rect.centerx - Borders.playerW / 2):
                        mobi.x -= mobi.speed
                    else:
                        mobi.x += mobi.speed
                else:
                    if (mobi.y > player.rect.centery - Borders.playerH / 2):
                        mobi.y -= mobi.speed
                    else:
                        mobi.y += mobi.speed
            for particle in mobi.spears:
                if particle.rect.colliderect(prect):
                    player.health -= particle.dmg
                    print(player.health)
                    particle.range = 0
                if particle.range == 0:
                    mobi.spears.remove(particle)
                else:
                    particle.main(player.direction.x * player.speed, player.direction.y * player.speed)

            mobi.main()

    for particle in playerParticles:
        flag = True
        for mobi in moblist:
            if mobi.isAlive and mobi.rect.colliderect(particle.rect):
                flag = False
                mobi.health -= particle.damage
                if (mobi.isAlive and mobi.health <= 0):
                    mobi.isAlive = False
                    player.gold += mobi.worth
                    mobi.x = mobi.homeX
                    mobi.y = mobi.homeY
                    mobi.deathTime = time.time()

        if particle.hasToExist and (flag or weapon_used.isMelee):
            particle.main(Screen, player.direction.x * player.speed, player.direction.y * player.speed)
        else:
            playerParticles.remove(particle)
    # pygame.draw.rect(Screen,(255,0,0),prect,4)
    # pygame.draw.rect(Screen,(0,0,255),rectScreen,20)

    i = 1
    # pygame.draw.rect(Screen, (50, 2, 5), prect,4)
    pygame.display.update()
    Clock.tick(60)
