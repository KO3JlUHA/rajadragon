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


def drawgold(gold, Acoin, Dcoin, Scoin):
    Screen.blit(Acoin, ((0, 1010), (70, 70)))
    Screen.blit(Dcoin, ((70, 1010), (70, 70)))
    Screen.blit(Scoin, ((35, 950), (70, 70)))
    toadd = ''
    if (gold >= 1000000000):
        gold = int(gold / 100000000)
        gold /= 10.0
        toadd = 'T'
    elif (gold >= 1000000):
        gold = int(gold / 100000)
        gold /= 10.0
        toadd = 'M'
    elif (gold >= 1000):
        gold = int(gold / 100)
        gold /= 10
        toadd = 'K'
    toShow = font.render(str(gold) + toadd, True, (255, 215, 0))
    Screen.blit(toShow, (140, 990))


# ------------------------------------------------------------------------------------ toGraphic
def drawhealth(health):  # 100*300
    ycord = Borders.screenH - 50
    xcord = (Borders.screenW / 2) - 150
    healthrect = pygame.Rect((xcord, ycord), (health * 3, 30))
    pygame.draw.rect(Screen, (0, 255, 0), healthrect)
    xcord += health * 3
    healthrect = pygame.Rect((xcord, ycord), ((100 - health) * 3, 30))
    pygame.draw.rect(Screen, (255, 0, 0), healthrect)


# ------------------------------------------------------------------------------------


class snowBall():
    def __init__(self, lvl):
        self.lvl = lvl
        self.dmg = self.lvl  # == lvl
        self.range = 60
        self.speed = 8
        self.cooldown = 0.25
        self.price = 10 * self.lvl
        self.upgradeCost = self.lvl * 15
        self.image = pygame.image.load("../images/weapons/snowball.png")
        self.isMelee = False
        self.icon = pygame.image.load('../images/icons/icon-cumball.png')

    def upgrate(self):
        if (player.gold >= self.upgradeCost and self.lvl < 998):
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
        self.image = pygame.image.load("../images/weapons/axe.png")
        self.image = pygame.transform.scale(self.image, (50, 140))
        self.icon = pygame.image.load('../images/icons/icon-axe.png')

    def upgrate(self):
        if (player.gold >= self.upgradeCost and self.lvl < 998):
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
        self.image = pygame.image.load("../images/weapons/arrow.png")
        self.isMelee = False
        self.icon = pygame.image.load('../images/icons/icon-bow.png')

    def upgrate(self):
        if (player.gold >= self.upgradeCost and self.lvl < 998):
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
        self.path = "../images/weapons/arrow.png"

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
    screenH = 1080
    screenW = 1920
    blockX = 60
    blockY = 60
    mapH = 0
    mapW = 0


class others():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = pygame.image.load("../images/basics/alienBlue_stand.png")
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
        self.image = pygame.image.load('../images/basics/alienBlue_stand.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (Borders.playerW, Borders.playerH))
        self.rect = self.image.get_rect(center=position)
        self.direction = pygame.math.Vector2()
        self.speed = 6

    def input(self):
        self.direction.x = 0
        self.direction.y = 0
        if (self.isTyping):
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and CameraGroup.offset.y + Borders.screenH / 2 - Borders.playerH / 2 > 0:
            self.direction.y -= 1
        if keys[pygame.K_s] and (CameraGroup.offset.y + CameraGroup.half_h) < Borders.mapH - Borders.playerH / 2:
            self.direction.y += 1

        if keys[pygame.K_d] and (CameraGroup.offset.x + CameraGroup.half_w) < Borders.mapW - Borders.playerW / 2:
            self.direction.x += 1
        if keys[pygame.K_a] and (CameraGroup.offset.x + CameraGroup.half_w) > Borders.playerW / 2:
            self.direction.x -= 1

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
        self.worth = 300
        self.isAlive = True
        self.health = health
        self.maxHealth = health
        self.deathTime = 0
        self.speed = speed
        self.timeOutOfRAnge = 0
        self.last_attack = 0
        self.spears = []
        self.images = pygame.image.load('../images/basics/mob.png').convert_alpha()
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
        self.groundSurf = pygame.image.load('../images/basics/ground2.jpg').convert_alpha()
        self.groundRect = self.groundSurf.get_rect(topleft=(0, 0))
        Borders.mapH = self.groundRect.height
        Borders.mapW = self.groundRect.width

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
Screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
Clock = pygame.time.Clock()

CameraGroup = CameraGroup()
player = Player((1000, 320), CameraGroup)
rectScreen = pygame.Rect((CameraGroup.offset.x, CameraGroup.offset.y), (1920, 1080))

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
arrow2 = bow(999)
ball2 = snowBall(420)
sur2 = axe(69)
weapons_list = ['', '', '', '', '', '']
weapons_list[0] = (arrow)
weapons_list[2] = (sur)
weapons_list[4] = (ball)
weapons_list[1] = (arrow2)
weapons_list[3] = (sur2)
weapons_list[5] = (ball2)
font = pygame.font.Font("freesansbold.ttf", 100)
fontlvl = pygame.font.Font("freesansbold.ttf", 20)
weapon_used = weapons_list[0]
last_attack = 0
prect = pygame.Rect((CameraGroup.half_w, CameraGroup.half_h), (Borders.playerW, Borders.playerH))
prect.center = (CameraGroup.half_w, CameraGroup.half_h)
rectScreen.center = prect.center
turn = 0
msg = ''
index = 1
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPClientSocket.sendto("!hi".encode(), serverAddressPort)
bytesToSend = str(player.rect.center).encode()
UDPClientSocket.sendto(bytesToSend, serverAddressPort)
# _____________________________________________________________________________
coinA = pygame.image.load('../images/coins/silver.png').convert_alpha()
coinD = pygame.image.load('../images/coins/bronze.png').convert_alpha()
coinA = pygame.transform.scale(coinA, (70, 70))
coinD = pygame.transform.scale(coinD, (70, 70))
coinS = pygame.image.load('../images/coins/gold.png').convert_alpha()
coinS = pygame.transform.scale(coinS, (70, 70))
# ______________________________________________________________________________
onfloor = []

while True:
    # _____________________________________________________________________________ check for death
    if player.health <= 0:
        UDPClientSocket.sendto('!L'.encode(), serverAddressPort)
        pygame.quit()
        sys.exit()
    # _____________________________________________________________________________

    # _____________________________________________________________________________ update camera
    Screen.fill('#71ddee')
    CameraGroup.update()
    CameraGroup.CustomDraw(player)
    # _____________________________________________________________________________ update deafolt values
    rectScreen.center = prect.center
    inventory = [weapons_list, player.gold]
    # _____________________________________________________________________________

    mouseX, mouseY = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
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
                    if ('!price'.startswith(msg) and len(msg) > 1):
                        msg = 'the upgrate price is: '
                        msg += str(weapon_used.upgradeCost)
                    print(msg)
                    # UDPClientSocket.sendto(msg.encode(), serverAddressPort)
                    msg = ''
            if not player.isTyping:
                if event.key == pygame.K_TAB:
                    pyautogui.press('volumeup', presses=100)
                    webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
                if event.key == pygame.K_1 and weapons_list[0] != '':
                    weapon_used = weapons_list[0]
                    index = 1
                elif event.key == pygame.K_2 and weapons_list[1] != '':
                    weapon_used = weapons_list[1]
                    index = 2
                elif event.key == pygame.K_3 and weapons_list[2] != '':
                    weapon_used = weapons_list[2]  # weapon choice   ↑
                    index = 3
                elif event.key == pygame.K_4 and weapons_list[3] != '':
                    weapon_used = weapons_list[3]  # weapon choice   ↑
                    index = 4
                elif event.key == pygame.K_5 and weapons_list[4] != '':
                    weapon_used = weapons_list[4]  # weapon choice   ↑
                    index = 5
                elif event.key == pygame.K_6 and weapons_list[5] != '':
                    weapon_used = weapons_list[5]  # weapon choice   ↑
                    index = 6
                elif event.key == pygame.K_u:
                    weapon_used.upgrate()
                elif event.key == pygame.K_x and weapon_used:  # drop the weapon
                    weapons_list[index - 1] = ''
                    tmp_dict = {'weapon': weapon_used, 'X': CameraGroup.offset.x + Borders.screenW / 2,
                                'Y': CameraGroup.offset.y + Borders.screenH / 2, 'rect': '', 'timeDropped': time.time()}
                    onfloor.append(tmp_dict)
                    tmp = 1
                    weapon_used = ''
                    if playerParticles and playerParticles[-1].speed == 0:
                        playerParticles = playerParticles[0:-1]
                    for weapon in weapons_list:
                        if weapon:
                            weapon_used = weapon
                            index = tmp
                            break
                        tmp += 1
                elif event.key == pygame.K_e:  # pick up weapon
                    flagT = True
                    for droped in onfloor:
                        if not flagT:
                            break
                        if prect.colliderect(droped['rect']):
                            for slot in weapons_list:
                                if not slot:
                                    weapons_list[weapons_list.index(slot)] = droped['weapon']
                                    onfloor.remove(droped)
                                    flagT = False
                                    break
                                    # hi
        if not player.isTyping:
            if event.type == pygame.MOUSEBUTTONDOWN and weapon_used:  # attack ↓
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
    for droped in onfloor:
        if droped['timeDropped'] + 10 <= time.time():
            onfloor.remove(droped)
        x = droped['X'] - CameraGroup.offset.x
        y = droped['Y'] - CameraGroup.offset.y
        weapon = droped["weapon"]
        rectt = pygame.Rect((x, y), (70, 70))
        droped['rect'] = rectt
        Screen.blit(weapon.icon, rectt)

    otherPlayer = []
    fleg = False
    for mobi in moblist:
        if len(mobi.spears) > 0:
            fleg = True

    if player.direction.x or player.direction.y or len(playerParticles) > 0 or fleg:
        bytesToSend = str(player.rect.center).encode()
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    reciven = UDPClientSocket.recvfrom(bufferSize)[0].decode()
    if reciven:
        reciven = reciven.replace('[', '')
        reciven = reciven.replace(']', '')
        reciven = reciven.replace("'", '')
        reciven = reciven.replace(' ', '')

        # here we have cords like 1486,1094, 1798,674
        for Pcords in reciven.split(','):
            if Pcords != 'TEMP' and Pcords != '!L':
                try:
                    (xcord, ycord) = Pcords.split('.')
                    xcord = int(xcord)
                    ycord = int(ycord)
                    player2 = others()
                    player2.x = xcord - CameraGroup.offset.x
                    player2.y = ycord - CameraGroup.offset.y
                    otherPlayer.append(player2)
                except:
                    pass
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
            if (mobi.rectTriger.colliderect(prect) and mobi.isAlive and turn != 0):
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
                    if player.health < 0:
                        player.health = 0
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
    rectt = pygame.Rect((1000, 900), (90, 90))
    rectt.bottomright = (1920, 1080)
    for i in range(6):
        pygame.draw.rect(Screen, (100, 100, 100), rectt, 10)
        if weapons_list[5 - i]:
            rectt.bottom += 10
            rectt.right += 10
            Screen.blit(weapons_list[5 - i].icon, rectt)
            toShow = fontlvl.render(str(weapons_list[5 - i].lvl), True, (0, 0, 100))
            Screen.blit(toShow, rectt)
            rectt.bottom -= 10
            rectt.right -= 10
        rectt.right -= 80
    for i in range(index):
        rectt.right += 80
    pygame.draw.rect(Screen, (255, 255, 255), rectt, 10)

    turn = 1
    drawhealth(player.health)
    drawgold(player.gold, coinA, coinD, coinS)
    pygame.display.update()
    Clock.tick(60)
