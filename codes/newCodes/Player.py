import math
import pygame


class Sizes:
    ScreenH = 1080
    ScreenW = 1920


class mob:
    def __init__(self, x, y, lvl, isMelley):#
        self.lastAttack = 0
        self.x = x
        self.y = y
        self.dir = 'r'
        self.homeX = x
        self.homeY = y
        self.lvl = lvl
        self.isMelley = isMelley
        self.isAlive = True
        self.DeathTime = 0
        self.health = 100 * lvl
        self.deathTime = 0
        # ---------------------- ranged --------------------------------
        # range = 600
        # speed = 5
        # dmg = 10
        # rect = pygame.Rect((x,y),(600,600))
        # rect.center = (x,y)
        # home_rect = pygame.Rect((x,y),(800,800))
        # home_recr.center = (x,y)
        # worth = 150*lvl

        # ---------------------- melley --------------------------------
        # range = on colidions
        # speed = 15
        # dmg = 14*lvl
        # rect = pygame.Rect((x,y),(1200,1200))
        # rect.center = (x,y)
        # home_rect = pygame.Rect((x,y),(1600,1600))
        # home_recr.center = (x,y)
        # worth = 300*lvl


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()

        self.offset = pygame.math.Vector2()
        self.half_w = self.displaySurface.get_size()[0] // 2
        self.half_h = self.displaySurface.get_size()[1] // 2

        self.groundSurf = pygame.image.load('../../images/basics/ground2.jpg').convert_alpha()
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


class Player(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)
        self.position = position
        self.image = pygame.image.load('../../images/basics/alienBlue_stand.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (66, 92))
        self.rect = self.image.get_rect(center=position)
        self.center = (0, 0)

    def update(self):
        self.rect.center = self.center

    def move(self):
        keys = pygame.key.get_pressed()
        dirX = 0
        dirY = 0
        if keys[pygame.K_w]:
            dirY -= 1

        if keys[pygame.K_s]:
            dirY += 1

        if keys[pygame.K_d]:
            dirX += 1

        if keys[pygame.K_a]:
            dirX -= 1
        return dirX, dirY


class PlayerParticle:
    def __init__(self, x, y, mouseX, mouseY, range, speed, name):
        self.x = x
        self.y = y
        self.mouseX = mouseX
        self.mouseY = mouseY
        self.speed = speed
        self.range = range
        self.angle = math.atan2(y - mouseY, x - mouseX)
        self.velocityX = math.cos(self.angle) * self.speed
        self.velocityY = math.sin(self.angle) * self.speed
        self.name = name
        self.Vx = self.velocityX
        self.Vy = self.velocityY
        self.Hit = False

    def main(self, x, y):
        if self.speed == 1:
            self.x = x
            self.y = y
            self.Vy += self.velocityY
            self.Vx += self.velocityX
        self.range -= self.speed
        self.x -= int(self.Vx)
        self.y -= int(self.Vy)

    # pygame.draw.circle(display, (0, 0, 0), (self.x - CameraGroup.offset.x, self.y - CameraGroup.offset.y), 5)
