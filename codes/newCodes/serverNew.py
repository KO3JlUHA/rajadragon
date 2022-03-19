import socket
import time
import weapons as wp
import pygame
import Player as pl

localIP = "0.0.0.0"
localPort = 20003
bufferSize = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to address and ip


UDPServerSocket.bind((localIP, localPort))
playes_speed = 6
players = []
particles = []
while True:
    left_flag = False
    final = ''
    rect = pygame.Rect((0, 0), (1920, 1080))
    rect.center = (960, 520)
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    msg = bytesAddressPair[0].decode()
    ip = bytesAddressPair[1]
    if msg == '!HI':  # "!HI"
        Data = {'IP': ip, 'X': 960, 'Y': 520, 'PARTICLES': [], 'HEALTH': 100, 'ATTACK-TIME': 0,
                'INVENTORY': [wp.weapon(1, 'bow'), "", "", "", "", ""], 'PICKED': 0, 'GOLD': 0}
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
            _, xDir, yDir = command.split('.')
            for player in players:
                if player['IP'] == ip:
                    x = int(player['X'])
                    y = int(player['Y'])
                    xDir = int(xDir)
                    yDir = int(yDir)
                    if command.startswith('!MOVE'):
                        if xDir < 0:
                            xDir = -1
                        elif xDir > 0:
                            xDir = 1
                        if yDir < 0:
                            yDir = -1
                        elif yDir > 0:
                            yDir = 1
                        x += playes_speed * xDir
                        y += playes_speed * yDir
                        rect = pygame.Rect((0, 0), (1920, 1080))
                        rect.center = (x, y)
                        player['X'] = x
                        player['Y'] = y
                        x = str(x)
                        y = str(y)
                        final = '!LOC|' + x + '|' + y
                    elif command.startswith('!ATTACK') and player['INVENTORY'][player['PICKED']]:
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
                            dmg = player['INVENTORY'][player['PICKED']].lvl * 2
                            name = 'snowball'
                        #  and player['INVENTORY'][player['PICKED']]
                        if player['ATTACK-TIME'] == 0 or player['ATTACK-TIME'] + cooldown <= time.time():
                            player['ATTACK-TIME'] = time.time()
                            player['PARTICLES'].append(
                                pl.PlayerParticle(int(player['X']), int(player['Y']), xDir, yDir, range, speed, name))
                        # particles.append(pl.PlayerParticle(int(player['X']),int(player['Y']),xDir,yDir))

    else:
        break
    final += "$!OTHER_p|"
    h = 0
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
    final += "$!PARTICLES|"

    for player in players:
        if player['PARTICLES']:
            for particle in player['PARTICLES']:
                for player2 in players:
                    if player2 != player:
                        x = int(player2['X'])
                        y = int(player2['Y'])
                        Prect = pygame.Rect((0, 0), (66, 92))
                        Prect.center = (x, y)
                        x = int(particle.x)
                        y = int(particle.y)
                        Wrect = pygame.Rect((0, 0), (50, 15))
                        Wrect.center = (x, y)
                        if Wrect.colliderect(Prect):
                            multiplier = 0
                            if player['INVENTORY'][player['PICKED']].name == 'bow':
                                multiplier = 6
                            elif player['INVENTORY'][player['PICKED']].name == 'snowball':
                                multiplier = 2
                            player2['HEALTH'] -= player['INVENTORY'][player['PICKED']].lvl * multiplier
                            player['PARTICLES'].remove(particle)
                if particle.range <= 0 and particle in player['PARTICLES']:
                    player['PARTICLES'].remove(particle)
                final += str(particle.x)
                final += '|'
                final += str(particle.y)
                final += '|'
                final += str(particle.angle)
                final += '|'
                final += str(particle.name)
                final += '@'
                particle.main()

    final += f'$!HEALTH|{h}'
    print(final)
    if not left_flag:
        UDPServerSocket.sendto(final.encode(), ip)
UDPServerSocket.close()
