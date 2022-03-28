import pygame
import sys
import math
import socket
import Player as Basics

class button():
    def __init__(self, img, X, Y):
        self.img = img
        self.X = X
        self.Y = Y

    def main(self, Screen, mouseRect, mouseButton):
        rect = self.img.get_rect()
        rect.center = self.X, self.Y
        Screen.blit(self.img, rect)

        if mouseButton and mouseRect.colliderect(rect):
            return True
        return False


imgArrow = pygame.image.load('../../images/weapons/arrow.png')
imgSnowball = pygame.image.load('../../images/weapons/snowball.png')
imgDragger = pygame.image.load('../../images/weapons/dagger.png')
iconBow = pygame.image.load('../../images/icons/icon-bow.png')
iconCumball = pygame.image.load('../../images/icons/icon-cumball.png')
imgSpear = pygame.image.load('../../images/weapons/spear.png')
iconDagger = pygame.transform.scale(pygame.image.load('../../images/icons/icon-dagger.png'), (70, 70))
imgDragger = pygame.transform.scale(imgDragger, (125, 40))

MobRange = pygame.image.load('../../images/basics/mob.png')
MobMeele = pygame.transform.scale(pygame.image.load('../../images/basics/zombie.png'), (88, 120))
mobRect = MobRange.get_rect()


sellImg = pygame.image.load('../../images/shop/sell.png')
sellObj = button(sellImg,960,200)


coinA = pygame.image.load('../../images/coins/silver.png')
coinD = pygame.image.load('../../images/coins/bronze.png')
coinA = pygame.transform.scale(coinA, (70, 70))
coinD = pygame.transform.scale(coinD, (70, 70))
coinS = pygame.image.load('../../images/coins/gold.png')
coinS = pygame.transform.scale(coinS, (70, 70))
Chat_Box = pygame.image.load('../../images/basics/chatBox.png')
Chat_Box = pygame.transform.scale(Chat_Box, (464, 30))


def drawgold(gold):
    Screen.blit(coinA, ((0, Basics.Sizes.ScreenH - 70), (70, 70)))
    Screen.blit(coinD, ((70, Basics.Sizes.ScreenH - 70), (70, 70)))
    Screen.blit(coinS, ((35, Basics.Sizes.ScreenH - 130), (70, 70)))
    toadd = ''
    if gold >= 1000000000:
        gold = int(gold / 100000000)
        gold /= 10.0
        toadd = 'T'
    elif gold >= 1000000:
        gold = int(gold / 100000)
        gold /= 10.0
        toadd = 'M'
    elif gold >= 1000:
        gold = int(gold / 100)
        gold /= 10
        toadd = 'K'
    toShow = font.render(str(gold) + toadd, True, (255, 215, 0))
    Screen.blit(toShow, (140, Basics.Sizes.ScreenH - 90))


def drawMob(x, y, isMelee, dir):
    mobRect.center = (x, y)
    if not isMelee:
        rtt = pygame.Rect((x,y),(600,600))
        Screen.blit(MobRange, mobRect)
    else:
        rtt = pygame.Rect((x, y), (1200, 1200))
        if dir == 'r':
            Screen.blit(pygame.transform.flip(MobMeele, True, False), mobRect)
        else:
            Screen.blit(MobMeele, mobRect)
    rtt.center=x,y
    pygame.draw.rect(Screen, (255, 0, 0), rtt, 4)
    mobiRect = pygame.Rect((0, 0), (88, 120))
    mobiRect.center = (x, y)
    pygame.draw.rect(Screen, (0, 255, 0), mobiRect, 4)



class others:
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
font = pygame.font.Font("freesansbold.ttf", 100)
fontlvl = pygame.font.Font("freesansbold.ttf", 20)
# Screen = pygame.display.set_mode((Basics.Sizes.ScreenW, Basics.Sizes.ScreenH))
Screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
Basics.Sizes.ScreenW, Basics.Sizes.ScreenH = Screen.get_size()

Clock = pygame.time.Clock()
CameraGroup = Basics.CameraGroup()
player = Basics.Player((640, 320), CameraGroup)
picked = 0
inventory = ['', '', '', '', '', 'FUCK']
mEvent = 0
inChat = False
inShop = False
ChatMsg = '$!CHAT|'
BlinkCounter = 0
msg = '$!CHAT|'

Chat_enabled = True


ms = pygame.transform.scale(pygame.image.load('../../images/basics/mouse.png'), (23, 36))
mouseRect = ms.get_rect()
while True:
    gold = 0
    Screen.fill('#71ddee')
    CameraGroup.update()
    CameraGroup.CustomDraw(player)
    # -------------------------------------------------------------
    pygame.mouse.set_visible(False)
    ChatRecieve = ''
    othersList = []
    reciven = UDPClientSocket.recvfrom(bufferSize)[0].decode()
    if reciven.__contains__('$!CHAT'):
        ChatRecieve = reciven[reciven.index('$!CHAT'):]
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
        elif command.startswith('!MOBS'):
            command = command[6:]
            for mob in command.split('@'):
                if mob:
                    x, y, isMeeley, dir = mob.split('|')
                    x = int(x) - CameraGroup.offset.x
                    y = int(y) - CameraGroup.offset.y
                    if isMeeley == 'True':
                        isMeeley = True
                    else:
                        isMeeley = False
                    drawMob(x, y, isMeeley, dir)
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
                        elif name == 'dagger':
                            img = imgDragger
                        img = pygame.transform.rotate(img, ANGLE)
                        rectTmp = img.get_rect()
                        rectTmp.center = (X - CameraGroup.offset.x, Y - CameraGroup.offset.y)
                        Screen.blit(img, rectTmp)
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
        elif command.startswith('!GOLD'):
            gold = int(command.split('|')[1])
        elif command.startswith('!SPEARS'):
            command = command[8:]
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
                    elif name == 'dagger':
                        img = imgDragger
                    elif name == 'spear':
                        img = imgSpear
                    img = pygame.transform.rotate(img, ANGLE)
                    rectTmp = img.get_rect()
                    rectTmp.center = (X - CameraGroup.offset.x, Y - CameraGroup.offset.y)
                    Screen.blit(img, rectTmp)
    if ChatRecieve and Chat_enabled:
        ChatRecieve = ChatRecieve[7:]
        heightTxt = 1
        while ChatRecieve:
            lenS = ChatRecieve.split("@")[0]
            len2 = len(lenS)+1
            lenS = int(lenS)
            txt = ChatRecieve[len2:]
            txt = txt[0:lenS]
            lenS+=len2
            ChatRecieve = ChatRecieve[lenS:]
            Screen.blit(fontlvl.render(txt, True, (255, 255, 255)), (1, heightTxt))
            heightTxt += 30#
    # pygame.draw.rect(Screen, (255, 0, 0), player.rect, 4)
    mouseX, mouseY = pygame.mouse.get_pos()
    mouseRect.topleft = (mouseX, mouseY)
    drawgold(gold)
    mouseXmap = int(mouseX + CameraGroup.offset.x)
    mouseYmap = int(mouseY + CameraGroup.offset.y)
    dirX = 0
    dirY = 0
    if not inChat:
        dirX, dirY = player.move()
    tosend = '!MOVE.' + str(dirX) + '.' + str(dirY)

    if inChat:
        Screen.blit(Chat_Box, (1, 145))
        blink = ''
        BlinkCounter += 1
        if BlinkCounter < 30:
            blink = '|'
        elif BlinkCounter >= 60:
            BlinkCounter = 0
        smthg = fontlvl.render(msg[7:] + blink, True, (255, 255, 255))
        Screen.blit(smthg, (7, 150))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            UDPClientSocket.sendto('!L'.encode(), serverAddressPort)
            pygame.quit()
            sys.exit()
        if inShop:
            mEvent = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                mEvent = event.button
        elif not inChat and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            tosend += f'$!ATTACK.{mouseXmap}.{mouseYmap}'
        if event.type == pygame.KEYDOWN:
            if inChat:
                pressed = ''
                try:
                    pressed = chr(event.key)
                    keys = pygame.key.get_pressed()
                    if (keys[pygame.K_BACKSPACE] and len(msg) > 7):
                        msg = msg[:-1]
                    elif (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                        if (pressed <= 'z' and pressed >= 'a'):
                            pressed = chr(event.key - 32)
                        elif pressed == '0':
                            pressed = ')'
                        elif pressed == '1':
                            pressed = '!'
                        elif pressed == '2':
                            pressed = '@'
                        elif pressed == '`':
                            pressed = '~'
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
                        elif pressed == '[':
                            pressed = '{'
                        elif pressed == ']':
                            pressed = '}'
                        elif pressed == '\\':
                            pressed = '|'

                except:
                    pass
                if len(msg) <= 50:
                    if pressed >= ' ' and pressed <= '~':
                        msg += str(pressed)

            if (event.key == pygame.K_RETURN or inChat)  and Chat_enabled:
                if event.key == pygame.K_RETURN:
                    inChat = not inChat
                if not inChat:
                    ChatMsg = msg
                    msg = '$!CHAT|'
            elif event.key == pygame.K_1:
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
            elif event.key == pygame.K_b:
                inShop = not inShop
            elif event.key == pygame.K_TAB:
                Chat_enabled = not Chat_enabled

    # if inShop:
    #     press = sellObj.main(Screen, mouseRect, mEvent)
    #     if press:
    #         print(press)


    if ChatMsg != '$!CHAT|':
        tosend += ChatMsg
        ChatMsg = '$!CHAT|'
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
            elif name == 'dagger':
                icon = iconDagger  #
            Screen.blit(icon, rectt)
            # toShow = fontlvl.render(str(weapons_list[5 - i].lvl), True, (0, 0, 100))
            Screen.blit(toShow, rectt)
            rectt.bottom -= 10
            rectt.right -= 10
        rectt.right -= 80
    for i in range(picked + 1):
        rectt.right += 80
    pygame.draw.rect(Screen, (255, 255, 255), rectt, 10)
    Screen.blit(ms, mouseRect)
    pygame.display.update()
    Clock.tick(60)
