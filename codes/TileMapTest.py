import csv
import os
import sys
import time

import pygame

tiles_per_line = 18
tile_size = 64


def read_csv(filename):
    map = []
    with open(os.path.join(filename)) as data:
        data = csv.reader(data, delimiter=',')
        for row in data:
            map.append(list(row))
    return map


def calcTopLeft(id: int):
    return id % tiles_per_line * tile_size, int(id / tiles_per_line) * tile_size


def tileDraw(xloc, yloc):
    x = 0
    y = 0
    for k in range(int(yloc / tile_size),
                   int(yloc / tile_size) + 18):  # cameraGroup.offset.y, cameraGroup.offset.y + 14
        for i in range(int(xloc / tile_size),
                       int(xloc / tile_size) + 31):  # cameraGroup.offset.x, cameraGroup.offset.x + 24
            try:
                x2, y2 = (calcTopLeft(int(map[k][i])))
                if k > 0 and i > 0:
                    Screen.blit(tile_set, (x * tile_size - xloc % tile_size, y * tile_size - yloc % tile_size),
                                (int(x2), int(y2), 64, 64))
            except:
                pass
            x += 1
        y += 1
        x = 0


pygame.init()
Screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
map = read_csv('GROUND1.csv')
tile_set = pygame.image.load('tileset64.png')
print(len(map), len(map[0]))
x, y = 32 + tile_size * 1100, 4 + tile_size * 600
player_speed = 8
COLIDELIST = [4, 5, 22, 23, 26, 39, 40, 41, 43, 57, 58, 59, 60, 75, 76, 77, 78, 92, 93, 94, 95, 96]
while running:
    # Screen.fill((81, 183, 250))
    Screen.fill('white')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
    # x3, y3 = 0, 0
    # for id in COLIDELIST:
    #     x2, y2 = (calcTopLeft(id))
    #     Screen.blit(tile_set, (x3 * tile_size, y3 * tile_size), (int(x2), int(y2), 64, 64))
    #     if x3 < 28:
    #         x3 += 1.1
    #     else:
    #         x3 = 0
    #         y3 += 1.1
    tileDraw(x, y)
    keys = pygame.key.get_pressed()
    r = pygame.Rect((0, 0), (64, 64))
    r.center = 960, 540
    pygame.draw.rect(Screen, (0, 255, 0), r, 4)
    r2 = pygame.Rect((960 - x % tile_size, 512 - y % tile_size), (64, 64))
    pygame.draw.rect(Screen, (255, 0, 0), r2, 4)
    if r2.y != r.y:
        if r2.y < r.y:
            r2.y += 64
        else:
            r2.y -= 64
        pygame.draw.rect(Screen, (255, 0, 0), r2, 4)
    if r2.x != r.x:
        if r2.x < r.x:
            r2.x += 64
            pygame.draw.rect(Screen, (255, 0, 0), r2, 4)
            if r2.y != r.y:
                if r2.y < r.y:
                    r2.y += 64
                else:
                    r2.y -= 64
                pygame.draw.rect(Screen, (255, 0, 0), r2, 4)
        else:
            r2.x -= 64
            pygame.draw.rect(Screen, (255, 0, 0), r2, 4)
            if r2.y != r.y:
                if r2.y < r.y:
                    r2.y += 64
                else:
                    r2.y -= 64
                pygame.draw.rect(Screen, (255, 0, 0), r2, 4)
    try:
        # if int(map[int((y + player_speed * (keys[pygame.K_s] - keys[pygame.K_w])) / tile_size) + 8][
        #            int((x + player_speed * (
        #                    keys[pygame.K_d] - keys[pygame.K_a])) / tile_size) + 15]) not in COLIDELIST:
        #     x += player_speed * (keys[pygame.K_d] - keys[pygame.K_a])
        #     y += player_speed * (keys[pygame.K_s] - keys[pygame.K_w])
        if not (x + 32) % tile_size:
            print('can collide x')
            if keys[pygame.K_d] - keys[pygame.K_a]:
                if keys[pygame.K_d]:
                    if int(map[int(y / tile_size) + 8][int(x / tile_size) + 16]) not in COLIDELIST:
                        x += player_speed
                else:
                    if int(map[int(y / tile_size) + 8][int(x / tile_size) + 14]) not in COLIDELIST:
                        x -= player_speed
        else:
            x += player_speed * (keys[pygame.K_d] - keys[pygame.K_a])
        if not (y - 4) % tile_size:
            print('can collide y')
            if keys[pygame.K_s] - keys[pygame.K_w]:
                if keys[pygame.K_s]:
                    if int(map[int(y / tile_size) + 9][int(x / tile_size) + 15]) not in COLIDELIST:
                        y += player_speed
                else:
                    if int(map[int(y / tile_size) + 7][int(x / tile_size) + 15]) not in COLIDELIST:
                        y -= player_speed
        else:
            y += player_speed * (keys[pygame.K_s] - keys[pygame.K_w])
    except:
        pass

    clock.tick(60)
    pygame.display.update()
