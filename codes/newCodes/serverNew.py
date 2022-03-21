import socket
import time
import weapons as wp
import pygame
import Player as pl

localIP = "0.0.0.0"
localPort = 20003
bufferSize = 1024
mobs = []
mob = pl.mob(200, 200, 2, False)
mobs.append(mob)
mob = pl.mob(100, 100, 5, False)
mobs.append(mob)

# Create a datagram socket
UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to address and ip

worth = 0
UDPServerSocket.bind((localIP, localPort))
player_speed = 6
players = []
rect = pygame.Rect((0, 0), (pl.Sizes.ScreenW, pl.Sizes.ScreenH))
while True:
    print(len(players))
    left_flag = False
    final = ''
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    msg = bytesAddressPair[0].decode()
    ip = bytesAddressPair[1]
    if msg == '!HI':  # "!HI"
        Data = {'IP': ip, 'X': 960, 'Y': 520, 'PARTICLES': [], 'HEALTH': 100, 'ATTACK-TIME': 0,
                'INVENTORY': [wp.weapon(1, 'bow'), wp.weapon(2, 'bow'), wp.weapon(3, 'snowball'),
                              wp.weapon(400, 'dagger'),
                              wp.weapon(5, 'bow'), wp.weapon(6, 'bow')], 'PICKED': 0, 'GOLD': 0}
        players.append(Data)
        final = '!LOC|960|520'
    elif msg == '!L':
        left_flag = True
        for player in players:
            if player['IP'] == ip:
                players.remove(player)
    elif msg.startswith("!MOVE"):  # mag = "!MOVE.DIRECTIONX.DIRECTIONTY$!ATTACK.MOUSEX.MOUSEY"
        commands = msg.split('$')
        for command in commands:
            for player in players:
                if player['IP'] == ip:
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
                        final = '!LOC|' + x + '|' + y
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

    else:
        break
    final += "$!OTHER_p|"
    h = 0
    pick = 0
    gold = 0
    inv = "$!INV|"
    for player in players:
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
            h = player['HEALTH']
            pick = player['PICKED']
            gold = player['GOLD']
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
                        if mobi.health <= 0 and mobi.isAlive:
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
                            elif player['INVENTORY'][player['PICKED']].name == 'dagger' and not particle.Hit:
                                particle.Hit = True
                                multiplier = 10
                            player2['HEALTH'] -= (player['INVENTORY'][player['PICKED']].lvl * multiplier)

    final += f'$!HEALTH|{h}'
    final += f'$!PICKED|{pick}'
    final += inv

    final += f'$!MOBS|'
    for mobi in mobs:
        if mobi.isAlive:
            mobiRect = pygame.Rect((0, 0), (88, 120))
            mobiRect.center = (mobi.x, mobi.y)
            if mobiRect.colliderect(rect):
                final += str(mobi.x)
                final += '|'
                final += str(mobi.y)
                final += '|'
                final += str(mobi.isMelley)
                final += '@'

    final += f'$!GOLD|{gold}'
    if players and ip == players[-1]['IP']:
        for player in players:
            if player['PARTICLES']:
                for particle in player['PARTICLES']:
                    particle.main(player['X'], player['Y'])

    if not left_flag:
        UDPServerSocket.sendto(final.encode(), ip)
UDPServerSocket.close()
