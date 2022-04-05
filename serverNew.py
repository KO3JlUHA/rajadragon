import math
import random
import socket
import time
import weapons as wp
import pygame
import Player as pl
import os
import csv

mobs = []


# mob = pl.mob(1200, 1200, 1, False)
# mobs.append(mob)
# mob = pl.mob(1100, 1100, 1, True)
# mobs.append(mob)


def read_csv(filename):
    map = []
    with open(os.path.join(filename)) as data:
        data = csv.reader(data, delimiter=',')
        for i, row in enumerate(data):
            map.append(list(row))
            for k, item in enumerate(row):
                if item == '67':
                    print(k * 64, i * 64)
                    mobs.append(pl.mob(k * 64 + 8, i * 64, 1, bool(random.randint(0, 1))))

    return map  #


map = read_csv('GROUND1.csv')
print(mobs)


def calcTime(time):
    days = int(time / 86400)
    time %= 86400
    hours = int(time / 3600)
    time %= 3600
    minutes = int(time / 60)
    time %= 60
    return f'{days}:{hours}:{minutes}:{time}'


StartTime = time.time()
localIP = "0.0.0.0"
localPort = 20003
bufferSize = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to address and ip
worth = 0
UDPServerSocket.bind((localIP, localPort))
player_speed = 8
players = []
spears = []
Chatmsg = []
rect = pygame.Rect((0, 0), (pl.Sizes.ScreenW, pl.Sizes.ScreenH))


def recv():
    pass


while True:
    left_flag = False
    final = ''
    chatPacket = ''
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    msg = bytesAddressPair[0].decode()
    ip = bytesAddressPair[1]
    if msg == '!HI':  # "!HI"
        Data = {'IP': ip, 'X': 33600, 'Y': 832, 'PARTICLES': [], 'HEALTH': 100, 'ATTACK-TIME': 0,
                'INVENTORY': [wp.weapon(1, 'bow'), wp.weapon(2, 'dagger'), wp.weapon(3, 'snowball'),
                              wp.weapon(10, 'dagger'),
                              wp.weapon(5, 'bow'), wp.weapon(6, 'snowball')], 'PICKED': 0, 'GOLD': 0,
                'LASTTIME': time.time()}
        players.append(Data)
        # final = '!LOC|960|520'
    elif msg == '!L':
        left_flag = True
        for player in players:
            if player['IP'] == ip:
                players.remove(player)
    elif msg.startswith("!MOVE"):  # mag = "!MOVE.DIRECTIONX.DIRECTIONTY$!ATTACK.MOUSEX.MOUSEY"
        if msg.__contains__('$!CHAT'):
            chatPacket = msg[msg.index('$!CHAT'):]
            msg = msg[:msg.index('$!CHAT')]
        commands = msg.split('$')
        for command in commands:
            for player in players:
                if player['IP'] == ip:
                    player['LASTTIME'] = time.time()
                    if command.startswith('!MOVE'):
                        _, xDir, yDir = command.split('.')
                        x = int(player['X'])
                        y = int(player['Y'])
                        xDir = int(xDir)
                        yDir = int(yDir)
                        if xDir < 0:
                            xDir = -1
                        elif xDir > 0:
                            xDir = 1
                        if yDir < 0:
                            yDir = -1
                        elif yDir > 0:
                            yDir = 1
                        x += player_speed * xDir
                        y += player_speed * yDir
                        rect.center = (x, y)
                        player['X'] = x
                        player['Y'] = y
                        x = str(x)
                        y = str(y)
                        # final = '!LOC|' + x + '|' + y
                    elif command.startswith('!ATTACK') and player['INVENTORY'][player['PICKED']]:
                        _, xDir, yDir = command.split('.')
                        x = int(player['X'])
                        y = int(player['Y'])
                        xDir = int(xDir)
                        yDir = int(yDir)
                        speed = 0
                        range = 0
                        cooldown = 0
                        dmg = 0
                        name = ''
                        if player['INVENTORY'][player['PICKED']].name == 'bow':
                            speed = 15
                            range = 700
                            cooldown = 2
                            dmg = player['INVENTORY'][player['PICKED']].lvl * 6
                            name = 'bow'
                        elif player['INVENTORY'][player['PICKED']].name == 'snowball':
                            speed = 10
                            range = 500
                            cooldown = 0.5
                            dmg = player['INVENTORY'][player['PICKED']].lvl
                            name = 'snowball'
                        elif player['INVENTORY'][player['PICKED']].name == 'dagger':
                            speed = 1
                            range = 60
                            cooldown = 4
                            dmg = player['INVENTORY'][player['PICKED']].lvl * 10
                            name = 'dagger'
                        #  and player['INVENTORY'][player['PICKED']]
                        if player['ATTACK-TIME'] == 0 or player['ATTACK-TIME'] + cooldown <= time.time():
                            player['ATTACK-TIME'] = time.time()
                            player['PARTICLES'].append(
                                pl.PlayerParticle(int(player['X']), int(player['Y']), xDir, yDir, range, speed, name))
                        # particles.append(pl.PlayerParticle(int(player['X']),int(player['Y']),xDir,yDir))
                    elif command.startswith('!PICK'):
                        index = command.split('.')[-1]
                        index = int(index)
                        if player['INVENTORY'][index]:
                            player['PICKED'] = index
    if chatPacket:
        print(chatPacket)
        chatPacket = chatPacket[7:]
        if len(Chatmsg) == 5:
            Chatmsg = Chatmsg[1:]
        Chatmsg.append({'TEXT': chatPacket, 'TIME': time.time() - StartTime})




    final += "$!OTHER_p|"
    playerThis = ''
    inv = "$!INV|"
    for player in players:
        if player['LASTTIME'] + 2 < time.time():
            players.remove(player)
        if player['IP'] != ip:
            x = int(player['X'])
            y = int(player['Y'])
            Prect = pygame.Rect((0, 0), (66, 92))
            Prect.center = (x, y)
            if Prect.colliderect(rect):
                final += str(x)
                final += '|'
                final += str(y)
                final += '@'
        else:
            playerThis = player
            for item in player['INVENTORY']:
                if item:
                    inv += str(item.lvl)
                    inv += '|'
                    inv += str(item.name)
                inv += '@'



    final += "$!PARTICLES|"

    for player in players:
        if player['PARTICLES']:
            for particle in player['PARTICLES']:
                x = int(particle.x)
                y = int(particle.y)
                xW = 0
                xH = 0
                if particle.name == 'bow':
                    xW = 50
                    xH = 15
                elif particle.name == 'snowball':
                    xW = 15
                    xH = 15
                elif particle.name == 'dagger':
                    xW = 120
                    xH = 40
                Wrect = pygame.Rect((0, 0), (xW, xH))
                Wrect.center = (x, y)
                if particle.range <= 0 and particle in player['PARTICLES']:
                    player['PARTICLES'].remove(particle)
                if Wrect.colliderect(rect):
                    final += str(particle.x)
                    final += '|'
                    final += str(particle.y)
                    final += '|'
                    final += str(particle.angle)
                    final += '|'
                    final += str(particle.name)
                    final += '@'
                for mobi in mobs:
                    if mobi.isAlive:
                        if mobi.health <= 0:
                            mobi.deathtime = time.time()
                            player['GOLD'] += worth
                            mobi.isAlive = False
                        x = int(mobi.x)
                        y = int(mobi.y)
                        Prect = pygame.Rect((0, 0), (88, 120))
                        Prect.center = (x, y)
                        if Wrect.colliderect(Prect):
                            multiplier = 0
                            if player['INVENTORY'][player['PICKED']].name == 'bow' and not particle.Hit:
                                particle.Hit = True
                                multiplier = 6
                                particle.range = 0
                            elif player['INVENTORY'][player['PICKED']].name == 'snowball' and not particle.Hit:
                                particle.Hit = True
                                multiplier = 1
                                particle.range = 0
                            elif player['INVENTORY'][player['PICKED']].name == 'dagger' and not particle.Hit:
                                particle.Hit = True
                                multiplier = 10
                            mobi.health -= (player['INVENTORY'][player['PICKED']].lvl * multiplier)

                            if mobi.isMelley:
                                worth = mobi.lvl * 300
                            else:
                                worth = mobi.lvl * 150

                for player2 in players:
                    if player2 != player:
                        x = int(player2['X'])
                        y = int(player2['Y'])
                        Prect = pygame.Rect((0, 0), (66, 92))
                        Prect.center = (x, y)
                        if Wrect.colliderect(Prect):
                            multiplier = 0
                            if player['INVENTORY'][player['PICKED']].name == 'bow' and not particle.Hit:
                                particle.Hit = True
                                multiplier = 6
                                particle.range = 0
                            elif player['INVENTORY'][player['PICKED']].name == 'snowball' and not particle.Hit:
                                particle.Hit = True
                                multiplier = 1
                                particle.range = 0
                            elif player['INVENTORY'][player['PICKED']].name == 'dagger' and not particle.Hit:
                                particle.Hit = True
                                multiplier = 10
                            player2['HEALTH'] -= (player['INVENTORY'][player['PICKED']].lvl * multiplier)

    if playerThis:
        final += f'$!PICKED|{playerThis["PICKED"]}'
    final += inv

    final += f'$!MOBS|'

    for mobi in mobs:
        if not mobi.isAlive and mobi.deathtime + 7 < time.time():
            mobi.x = mobi.homeX
            mobi.y = mobi.homeY
            mobi.health = 100 * mobi.lvl
            mobi.isAlive = True
        if mobi.isAlive:
            trig = 0
            if mobi.isMelley:
                trig = 1200
            else:
                trig = 600
            TrigRect = pygame.Rect((0, 0), (trig, trig))
            TrigRect.center = (mobi.x, mobi.y)
            speed = 5
            if mobi.isMelley:
                speed = 20

            flag_move = False
            px = 0
            py = 0
            rng = 10000

            for player in players:
                PlayerRect = pygame.Rect((0, 0), (66, 92))
                PlayerRect.center = (player['X'], player['Y'])
                if TrigRect.colliderect(PlayerRect):
                    Px, Py = PlayerRect.center
                    if mobi.lastAttack + 2 < time.time():
                        mobi.lastAttack = time.time()
                        if not mobi.isMelley:
                            spears.append(pl.PlayerParticle(mobi.x, mobi.y, Px, Py, 500, 30, 'spear'))  # spear later
                        else:
                            mobiRect = pygame.Rect((0, 0), (88, 120))
                            mobiRect.center = (mobi.x, mobi.y)
                            if PlayerRect.colliderect(mobiRect):
                                player['HEALTH'] -= 10
                    if math.sqrt((mobi.x - Px) ** 2 + (mobi.y - Py) ** 2) < rng:
                        px = Px
                        py = Py
                        rng = math.sqrt((mobi.x - Px) ** 2 + (mobi.y - Py) ** 2)

                    x = random.randint(0, 1)
                    if x == 0:
                        if mobi.x > px:
                            mobi.x -= speed
                            mobi.dir = 'l'
                        else:
                            mobi.x += speed
                            mobi.dir = 'r'
                    else:
                        if mobi.y > py:
                            mobi.y -= speed
                        else:
                            mobi.y += speed

                    flag_move = True
                    break
            if not flag_move:
                x = random.randint(0, 1)
                if x == 0:
                    if mobi.x > mobi.homeX:
                        mobi.x -= speed
                        mobi.dir = 'l'
                    elif mobi.x < mobi.homeX:
                        mobi.x += speed
                        mobi.dir = 'r'
                else:
                    if mobi.y > mobi.homeY:
                        mobi.y -= speed
                    elif mobi.y < mobi.homeY:
                        mobi.y += speed

            mobiRect = pygame.Rect((0, 0), (88, 120))
            mobiRect.center = (mobi.x, mobi.y)
            if mobiRect.colliderect(rect):
                final += str(mobi.x)
                final += '|'
                final += str(mobi.y)
                final += '|'
                final += str(mobi.isMelley)
                final += '|'
                final += str(mobi.dir)
                final += '@'

    if playerThis:
        final += f'$!GOLD|{playerThis["GOLD"]}'
    final += '$!SPEARS|'

    if playerThis:
        for particle in spears:
            Wrect = pygame.Rect((0, 0), (50, 15))
            Wrect.center = (particle.x, particle.y)
            if Wrect.colliderect(rect):
                final += str(particle.x)
                final += '|'
                final += str(particle.y)
                final += '|'
                final += str(particle.angle)
                final += '|'
                final += str(particle.name)
                final += '@'
                PlayerRect = pygame.Rect((0, 0), (66, 92))
                PlayerRect.center = rect.center
                if PlayerRect.colliderect(Wrect) and not particle.Hit:
                    particle.Hit = True
                    playerThis['HEALTH'] -= 10
                    particle.range = 0

    if playerThis:
        final += f'$!HEALTH|{playerThis["HEALTH"]}'

    if not playerThis:
        spears = []
        for mobi in mobs:
            mobi.x = mobi.homeX
            mobi.y = mobi.homeY
    if players and ip == players[-1]['IP']:
        for spear in spears:
            if spear.range == 0:
                spears.remove(spear)
            spear.main(0, 0)  #

        for player in players:
            if player['PARTICLES']:
                for particle in player['PARTICLES']:
                    particle.main(player['X'], player['Y'])

    if Chatmsg:
        final += '$!CHAT|'
        for msg in Chatmsg:
            if msg['TIME'] + 10 <= time.time() - StartTime:
                Chatmsg.remove(msg)
            mmssgg = msg['TEXT'] + ' [' + calcTime(int(msg['TIME'])) + ']'
            # mmssgg = msg['NAME']+': ' +msg['TEXT'] + ' [' + calcTime(int(msg['TIME'])) + ']'
            final += str(len(mmssgg)) + '@' + mmssgg

    if not left_flag:
        final = f'!LOC|{playerThis["X"]}|{playerThis["Y"]}{final}'
        print(final)
        UDPServerSocket.sendto(final.encode(), ip)
UDPServerSocket.close()