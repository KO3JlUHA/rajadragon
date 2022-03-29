import pygame
import sys
import math
import socket
import Player as Basics
import random



offerImg = pygame.image.load('../../images/shop/offer.png')
offerImg = pygame.transform.scale(offerImg, (offerImg.get_size()[0] * 1.25, offerImg.get_size()[1] * 1.25))
buy_img = pygame.image.load('../../images/shop/buy.png')
buy_img = pygame.transform.scale(buy_img, (buy_img.get_size()[0] / 1.7, buy_img.get_size()[1] / 1.7))
sell_img = pygame.image.load('../../images/shop/sell.png')
sell_img = pygame.transform.scale(sell_img, (sell_img.get_size()[0] / 1.7, sell_img.get_size()[1] / 1.7))


upgrade_img = pygame.image.load('../../images/shop/upgrade.png')

upgrade_img = pygame.transform.scale(upgrade_img, (upgrade_img.get_size()[0] / 1.7, upgrade_img.get_size()[1] / 1.7))

class button():
    def __init__(self, img, X, Y, lvl, dmg, cooldown, range, upgrade, sell, price):
        self.img = img
        self.X = X
        self.Y = Y
        self.clicked = False
        self.lvl = lvl

        self.dmg = dmg
        self.cooldown = cooldown
        self.range = range
        self.upgrade = upgrade
        self.sell = sell
        self.price = price

    def main(self):
        rect = self.img.get_rect()
        rect.topleft = self.X, self.Y
        # Screen.blit(self.img, rect)
        if pygame.mouse.get_pressed()[0] == 1 and not self.clicked and rect.collidepoint(pygame.mouse.get_pos()):
            self.clicked = True
            return True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return False

    def showOffer(self):
        Screen.blit(offerImg, (0, 0))
        txtt = fontShop.render(self.lvl, True, (255, 20, 30))
        rt = txtt.get_rect()
        rt.topright = (347, 211)
        Screen.blit(txtt, rt)

        txtt = fontShop.render(self.dmg, True, (255, 20, 30))
        rt = txtt.get_rect()
        rt.topright = (347, 268)
        Screen.blit(txtt, rt)

        txtt = fontShop.render(self.cooldown, True, (255, 20, 30))
        rt = txtt.get_rect()
        rt.topright = (347, 322)
        Screen.blit(txtt, rt)

        txtt = fontShop.render(self.range, True, (255, 20, 30))
        rt = txtt.get_rect()
        rt.topright = (347, 377)
        Screen.blit(txtt, rt)

        if self.price != '0':
            Screen.blit(buy_img, (25, 60))
            if not buySellOrUpgrade:
                buySellOrUpgrade.append(button(buy_img, 25, 60, 0, 0, 0, 0, 0, 0, 0))

            txtt = fontShop.render(self.price, True, (255, 20, 30))
            rt = txtt.get_rect()
            rt.topright = (341, 60)
            Screen.blit(txtt, rt)

        if self.upgrade != '0':
            if not buySellOrUpgrade:
                buySellOrUpgrade.append(button(upgrade_img, 25, 10, 0,0,0,0,0,0,0))
                buySellOrUpgrade.append(button(sell_img, 25, 120, 0, 0, 0, 0, 0, 0, 0))
            Screen.blit(upgrade_img, (25, 10))
            Screen.blit(sell_img, (25, 120))


            txtt = fontShop.render(self.upgrade, True, (255, 20, 30))
            rt = txtt.get_rect()
            rt.topright = (341, 60)
            Screen.blit(txtt, rt)

            txtt = fontShop.render(self.sell, True, (255, 20, 30))
            rt = txtt.get_rect()
            rt.topright = (341, 120)
            Screen.blit(txtt, rt)

        # print(len(buySellOrUpgrade))
        for buttonOrSmthg in buySellOrUpgrade:
            if buttonOrSmthg.main():
                if len(buySellOrUpgrade)==1:
                    print('buy pressed')
                elif buySellOrUpgrade.index(buttonOrSmthg)==0:
                    print('upgrade pressed')
                else:
                    print('sell pressed')
            #add blits of sell and upgrade


ShopImg = pygame.image.load('../../images/shop/shop.png')
# ShopImg = pygame.transform.scale(ShopImg, (1600, 900))
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
        rtt = pygame.Rect((x, y), (600, 600))
        Screen.blit(MobRange, mobRect)
    else:
        rtt = pygame.Rect((x, y), (1200, 1200))
        if dir == 'r':
            Screen.blit(pygame.transform.flip(MobMeele, True, False), mobRect)
        else:
            Screen.blit(MobMeele, mobRect)
    rtt.center = x, y
    pygame.draw.rect(Screen, (255, 0, 0), rtt, 4)
    mobiRect = pygame.Rect((0, 0), (88, 120))
    mobiRect.center = (x, y)
    pygame.draw.rect(Screen, (0, 255, 0), mobiRect, 4)


def getItem():
    rnd = random.randint(0, 2)
    if rnd == 0:
        return 'bow', iconBow, 6, 2, 700, 150
    elif rnd == 1:
        return 'snowball', iconCumball, 2, 0.5, 600, 50
    else:
        return 'dagger', iconDagger, 10, 1, 120, 100


def getLvl(most_upgrated):
    rnd = random.randint(-10, 10)
    lvl = most_upgrated + rnd
    if lvl < 1:
        lvl = 1
    return lvl


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
fontShop = pygame.font.Font(None, 70)
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
Chat_enabled_tmp = True

most_upgrated_old = -1

lvlForOffer = 0
itemForOffer = ''
imgOffer = ''
dmg1 = 0
range1 = 0
cooldown1 = 0
price1 = 0

ms = pygame.transform.scale(pygame.image.load('../../images/basics/mouse.png'), (23, 36))
mouseRect = ms.get_rect()

offer_buttons = []
most_upgrated = 0
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
            len2 = len(lenS) + 1
            lenS = int(lenS)
            txt = ChatRecieve[len2:]
            txt = txt[0:lenS]
            lenS += len2
            ChatRecieve = ChatRecieve[lenS:]
            Screen.blit(fontlvl.render(txt, True, (255, 255, 255)), (1, heightTxt))
            heightTxt += 30  #
    # pygame.draw.rect(Screen, (255, 0, 0), player.rect, 4)
    mouseX, mouseY = pygame.mouse.get_pos()
    mouseRect.topleft = (mouseX, mouseY)
    drawgold(gold)
    mouseXmap = int(mouseX + CameraGroup.offset.x)
    mouseYmap = int(mouseY + CameraGroup.offset.y)
    dirX = 0
    dirY = 0
    if not inChat and not inShop:
        dirX, dirY = player.move()
    tosend = '!MOVE.' + str(dirX) + '.' + str(dirY)

    if inShop:
        rt = ShopImg.get_rect()
        rt.center = (Basics.Sizes.ScreenW / 2, Basics.Sizes.ScreenH / 2)
        Screen.blit(ShopImg, rt)

        rt = imgOffer.get_rect()
        rt.center = (Basics.Sizes.ScreenW / 2, Basics.Sizes.ScreenH / 2 - 100)  # rt stays to be teh offers rect
        Screen.blit(imgOffer, rt)

        if not offer_buttons:
            offer_buttons.append(
                button(imgOffer, rt.x, rt.y, str(lvlForOffer), str(dmg1 * int(lvlForOffer)), str(cooldown1), str(
                    range1), '0', '0', str(int(
                    lvlForOffer) * price1)))  # def __init__(self, img, X, Y, lvl, dmg, cooldown, range, buy, upgrade, sell):

        startcordsX = Basics.Sizes.ScreenW / 2 - 395
        startcordsY = Basics.Sizes.ScreenH / 2 + 20
        for item in inventory:
            lvl, name = item.split('|')
            icon = iconBow
            dmg2 = 6*int(lvl)
            cooldown2 = 2
            range2 = 700
            upgrade_price = 140*int(lvl)
            sell_price = 130*int(lvl)
            if name == 'snowball':
                icon = iconCumball
                dmg2 = int(lvl) * 2
                cooldown2 = 0.5
                range2 = 600
                upgrade_price = 40 * int(lvl)
                sell_price = 30 * int(lvl)
            elif name == 'dagger':
                icon = iconDagger  #
                dmg2 = int(lvl) * 10
                cooldown2 = 1
                range2 = 120
                upgrade_price = 90 * int(lvl)
                sell_price = 80 * int(lvl)
            dmg2 = str(dmg2)
            cooldown2 = str(cooldown2)
            range2 = str(range2)
            upgrade_price = str(upgrade_price)
            sell_price = str(sell_price)
            if len(offer_buttons) < 7:
                offer_buttons.append(button(icon, startcordsX, startcordsY, lvl, dmg2,  cooldown2, range2, upgrade_price, sell_price, '0'))
            Screen.blit(icon, (startcordsX, startcordsY))
            startcordsX += 145

        for offer_button in offer_buttons:
            if offer_button.clicked:
                offer_button.showOffer()
            else:
                if offer_button.main():
                    buySellOrUpgrade = []
                    offer_button.showOffer()
                    for offer2 in offer_buttons:
                        if offer2 != offer_button:
                            offer2.clicked = False

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
        elif not inChat and not inShop and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
            if (event.key == pygame.K_RETURN or inChat) and Chat_enabled and not inShop:
                if event.key == pygame.K_RETURN:
                    inChat = not inChat
                if not inChat:
                    ChatMsg = msg
                    msg = '$!CHAT|'
            elif event.key == pygame.K_b or inShop:
                if event.key == pygame.K_b:
                    inShop = not inShop
                    if inShop:
                        if most_upgrated != most_upgrated_old:
                            most_upgrated_old = most_upgrated
                            lvlForOffer = getLvl(most_upgrated)
                            itemForOffer, imgOffer, dmg1, cooldown1, range1, price1 = getItem()
                        Chat_enabled_tmp = Chat_enabled
                        Chat_enabled = False
                        buySellOrUpgrade = []
                    else:
                        offer_buttons = []
                        Chat_enabled = Chat_enabled_tmp
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
            elif event.key == pygame.K_TAB:
                Chat_enabled = not Chat_enabled

    # if inShop:
    #     press = sellObj.main(Screen, (mouseX, mouseY), mEvent)
    #     if press:
    #         print(press)

    if ChatMsg != '$!CHAT|':
        tosend += ChatMsg
        ChatMsg = '$!CHAT|'
    UDPClientSocket.sendto(tosend.encode(), serverAddressPort)

    rectt = pygame.Rect((1000, 900), (90, 90))
    rectt.bottomright = (Basics.Sizes.ScreenW, Basics.Sizes.ScreenH)
    c = 0
    most_upgrated = 0
    for i in range(6):
        pygame.draw.rect(Screen, (100, 100, 100), rectt, 10)
        if inventory[5 - i]:
            c += 1
            rectt.bottom += 10
            rectt.right += 10
            lvl, name = inventory[5 - i].split('|')
            most_upgrated += int(lvl)
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
    most_upgrated /= c
    most_upgrated = int(most_upgrated)
    for i in range(picked + 1):
        rectt.right += 80
    pygame.draw.rect(Screen, (255, 255, 255), rectt, 10)
    Screen.blit(ms, mouseRect)
    pygame.display.update()
    Clock.tick(60)
