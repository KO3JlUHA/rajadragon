import pygame
import sys
import math

class Collisions():
        playerH = 92
        playerW = 66
        screenH = 1300
        screenW = 1950
        blockX = 60
        blockY = 60

class Player(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)
        self.health
        self.position = position
        self.image = pygame.image.load('alienBlue_stand.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (Collisions.playerW, Collisions.playerH))
        self.rect = self.image.get_rect(center=position)
        self.direction = pygame.math.Vector2()
        self.speed = 6

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and (CameraGroup.offset.y + CameraGroup.half_h) > Collisions.playerH/2:
            self.direction.y = -1
        elif keys[pygame.K_s] and (CameraGroup.offset.y + CameraGroup.half_h) < Collisions.screenH - Collisions.playerH/2:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d] and (CameraGroup.offset.x + CameraGroup.half_w) < Collisions.screenW - Collisions.playerW/2:
            self.direction.x = 1
        elif keys[pygame.K_a] and (CameraGroup.offset.x + CameraGroup.half_w) > Collisions.playerW/2:
            self.direction.x = -1
        else:
            self.direction.x = 0


    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed


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
    def __init__(self, x, y, mouseX, mouseY):
        self.x = x
        self.y = y
        self.mouseX = mouseX
        self.mouseY = mouseY
        self.speed = 15
        self.angle = math.atan2(y - mouseY, x - mouseX)
        self.velocityX = math.cos(self.angle) * self.speed
        self.velocityY = math.sin(self.angle) * self.speed

    def main(self, display, directionX, directionY):
        self.x -= int(self.velocityX + directionX)
        self.y -= int(self.velocityY + directionY)
        pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), 5)


pygame.init()
Screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
Clock = pygame.time.Clock()

CameraGroup = CameraGroup()
player = Player((640, 320), CameraGroup)
playerParticle = []
while True:
    if CameraGroup.offset.x == 0 and CameraGroup.offset.y == 0:
        pygame.draw.rect(Screen, (255, 0, 0), (0, 0, 500, 500))
    mouseX, mouseY = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                playerParticle.append(PlayerParticle(CameraGroup.half_w, CameraGroup.half_h, mouseX, mouseY))



    Screen.fill('#71ddee')
    CameraGroup.update()
    CameraGroup.CustomDraw(player)
    for particle in playerParticle:
        particle.main(Screen, player.direction.x * player.speed, player.direction.y * player.speed)

    pygame.display.update()
    Clock.tick(60)
