import math
import random
import socket
import time
import weapons as wp
import pygame
import Player as pl
import os
import csv
import threading

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
                    mobs.append(pl.mob(k * 64 + 30, i * 64 + 20, 1, bool(random.randint(0, 1))))

    return map  #


map = read_csv('GROUND1.csv')


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
ips = []


def move_mobs():
    for spear in spears:
        Wrect = pygame.Rect((0, 0), (50, 15))
        Wrect.center = (spear.x, spear.y)
        if spear.range <= 0:
            spears.remove(spear)
        spear.main(0, 0)
        for player in players:
            PlayerRect = pygame.Rect((0, 0), (66, 92))
            PlayerRect.center = rect.center
            if PlayerRect.colliderect(Wrect) and not spear.Hit:
                spear.Hit = True
                player['HEALTH'] -= 10
                spear.range = 0

    for mobi in mobs:
        if not mobi.isAlive and mobi.deathtime + 7 < time.time():
            mobi.x = mobi.homeX
            mobi.y = mobi.homeY
            mobi.health = 100 * mobi.lvl
            mobi.isAlive = True
        if mobi.isAlive:
            mobiRect = pygame.Rect((0, 0), (88, 120))
            mobiRect.center = (mobi.x, mobi.y)
            for player in players:
                for particle in player['PARTICLES']:
                    width = 0
                    height = 0
                    if particle.name == 'bow':
                        width = 50
                        height = 15
                    elif particle.name == 'snowball':
                        width = 15
                        height = 15
                    elif particle.name == 'dagger':
                        width = 120
                        height = 40

                    particle_rect = pygame.Rect((0, 0), (width, height))
                    particle_rect.center = particle.x, particle.y
                    for player2 in players:
                        if player2['IP'] != player['IP']:
                            player_rect = pygame.Rect((0, 0), (66, 92))
                            player_rect.center = player2['X'], player2['Y']
                            if player_rect.colliderect(particle_rect):
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

                    if particle_rect.colliderect(mobiRect):
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

                        if mobi.health <= 0:
                            mobi.isAlive = False
                            mobi.deathtime = time.time()
                            player['GOLD'] += worth

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


def recv():
    chatPacket = ''
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    msg = bytesAddressPair[0].decode()
    print(msg)
    ip = bytesAddressPair[1]
    if msg == '!HI':  # "!HI"
        ips.append(ip)
        Data = {'IP': ip, 'X': 33600, 'Y': 832, 'PARTICLES': [], 'HEALTH': 100, 'ATTACK-TIME': 0,
                'INVENTORY': [wp.weapon(100, 'bow'), wp.weapon(2, 'dagger'), wp.weapon(300, 'snowball'),
                              wp.weapon(10, 'dagger'),
                              wp.weapon(5, 'bow'), wp.weapon(6, 'snowball')], 'PICKED': 0, 'GOLD': 0,
                'LASTTIME': time.time()}
        players.append(Data)
        # final = '!LOC|960|520'
    elif msg == '!L':
        for player in players:
            if player['IP'] == ip:
                ips.remove(ip)
                players.remove(player)
        return
    elif msg.startswith("!MOVE"):  # mag = "!MOVE.DIRECTIONX.DIRECTIONTY$!ATTACK.MOUSEX.MOUSEY"
        if msg.__contains__('$!CHAT'):
            chatPacket = msg[msg.index('$!CHAT'):]
            msg = msg[:msg.index('$!CHAT')]
        commands = msg.split('$')
        for command in commands:
            player = players[ips.index(ip)]
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
                player['X'] = x
                player['Y'] = y
            elif command.startswith('!ATTACK') and player['INVENTORY'][player['PICKED']]:
                _, xDir, yDir = command.split('.')
                xDir = int(xDir)
                yDir = int(yDir)
                speed = 0
                range = 0
                cooldown = 0
                name = ''
                if player['INVENTORY'][player['PICKED']].name == 'bow':
                    speed = 15
                    range = 700
                    cooldown = 2
                    name = 'bow'
                elif player['INVENTORY'][player['PICKED']].name == 'snowball':
                    speed = 10
                    range = 500
                    cooldown = 0.5
                    name = 'snowball'
                elif player['INVENTORY'][player['PICKED']].name == 'dagger':
                    speed = 1
                    range = 60
                    cooldown = 4
                    name = 'dagger'
                #  and player['INVENTORY'][player['PICKED']]
                if player['ATTACK-TIME'] == 0 or player['ATTACK-TIME'] + cooldown <= time.time():
                    player['ATTACK-TIME'] = time.time()
                    player['PARTICLES'].append(
                        pl.PlayerParticle(int(player['X']), int(player['Y']), xDir, yDir, range, speed, name))
            elif command.startswith('!PICK'):
                index = command.split('.')[-1]
                index = int(index)
                if player['INVENTORY'][index]:
                    player['PICKED'] = index
    if chatPacket:
        chatPacket = chatPacket[7:]
        Chatmsg.append({'TEXT': chatPacket, 'TIME': time.time() - StartTime})


def send():
    for x, ip in enumerate(ips):
        gold = '$!GOLD|'
        picked = '$!PICKED|'
        health = '$!HEALTH|'
        mobsStr = '$!MOBS|'
        spearsStr = '$!SPEARS|'
        inv = "$!INV|"
        others = "$!OTHER_p|"

        particlesStr = '$!PARTICLES|'
        packet = f'!LOC|{players[x]["X"]}|{players[x]["Y"]}'

        rect = pygame.Rect((players[x]["X"], players[x]["Y"]), (1920, 1080))
        rect.center = (players[x]["X"], players[x]["Y"])
        for player in players:
            if player['PARTICLES']:
                for particle in player['PARTICLES']:
                    particle.main(player['X'], player['Y'])
                    if particle.range <= 0:
                        player['PARTICLES'].remove(particle)
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
                    if Wrect.colliderect(rect):
                        particlesStr += f'{particle.x}|{particle.y}|{particle.angle}|{particle.name}@'
            if player['IP'] != ip:
                x = int(player['X'])
                y = int(player['Y'])
                Prect = pygame.Rect((0, 0), (66, 92))
                Prect.center = (x, y)
                if Prect.colliderect(rect):
                    others += f'{x}|{y}@'
            else:
                health += str(player['HEALTH'])
                gold += f"{player['GOLD']}"
                picked += str(player['PICKED'])
                for item in player['INVENTORY']:
                    if item:
                        inv += f'{item.lvl}|{item.name}'
                    inv += '@'

        for mobi in mobs:
            if mobi.isAlive:
                mobiRect = pygame.Rect((0, 0), (88, 120))
                mobiRect.center = (mobi.x, mobi.y)
                if mobiRect.colliderect(rect):
                    mobsStr += f'{mobi.x}|{mobi.y}|{mobi.isMelley}|{mobi.dir}@'

        for particle in spears:
            Wrect = pygame.Rect((0, 0), (50, 15))
            Wrect.center = (particle.x, particle.y)
            if Wrect.colliderect(rect):
                spearsStr += f'{particle.x}|{particle.y}|{particle.angle}|{particle.name}@'

        if others != "$!OTHER_p|":
            packet += others

        if particlesStr != '$!PARTICLES|':
            packet += particlesStr

        if picked != '$!PICKED|':
            packet += picked

        if inv != '$!INV|':
            packet += inv

        if mobsStr != '$!MOBS|':
            packet += mobsStr

        if gold != '$!GOLD|':
            packet += gold
        if health != '$!HEALTH|':
            packet += health

        if spearsStr != '$!SPEARS|':
            packet += spearsStr

        if Chatmsg:
            packet += '$!CHAT|'
            for msg in Chatmsg:
                if msg['TIME'] + 10 <= time.time() - StartTime:
                    Chatmsg.remove(msg)
                mmssgg = msg['TEXT'] + ' [' + calcTime(int(msg['TIME'])) + ']'
                # mmssgg = msg['NAME']+': ' +msg['TEXT'] + ' [' + calcTime(int(msg['TIME'])) + ']'
                packet += str(len(mmssgg)) + '@' + mmssgg

        UDPServerSocket.sendto(packet.encode(), ip)


while True:
    # print(threading.active_count() - 1, len(ips))
    for _ in range(len(ips) + 2 - threading.active_count()):
        threading.Thread(target=recv).start()
    if len(Chatmsg) == 6:
        Chatmsg = Chatmsg[1:]
    send()
    move_mobs()
