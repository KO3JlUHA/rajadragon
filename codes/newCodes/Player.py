import math
import pygame


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
        dir = [dirX, dirY]
        return dir


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

    def main(self):
        self.range -= self.speed
        self.x -= int(self.velocityX)
        self.y -= int(self.velocityY)
        # pygame.draw.circle(display, (0, 0, 0), (self.x - CameraGroup.offset.x, self.y - CameraGroup.offset.y), 5)
