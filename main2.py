import pygame
import sys
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)
        self.position = position
        self.image = pygame.image.load('alienBlue_stand.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (66, 92))
        self.rect = self.image.get_rect(center=position)
        self.direction = pygame.math.Vector2()
        self.speed = 6

    def update(self):
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

    def main(self, display):
        self.x -= int(self.velocityX)
        self.y -= int(self.velocityY)
        pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), 5)


pygame.init()
Screen = pygame.display.set_mode((1280, 720))
Clock = pygame.time.Clock()

CameraGroup = CameraGroup()
player = Player((640, 320), CameraGroup)

playerParticle = []
while True:
    mouseX, mouseY = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                playerParticle.append(PlayerParticle(player.position[0] + 20, player.position[1] + 50, mouseX, mouseY))

    if keys[pygame.K_w]:
        player.direction.y = -1

    elif keys[pygame.K_s]:
        player.direction.y = 1

    else:
        player.direction.y = 0

    if keys[pygame.K_d]:
        player.direction.x = 1

    elif keys[pygame.K_a]:
        player.direction.x = -1

    elif keys[pygame.K_LSHIFT]:
        player.speed += 5

    else:
        player.direction.x = 0

    Screen.fill('#71ddee')
    CameraGroup.update()
    CameraGroup.CustomDraw(player)
    for particle in playerParticle:
        particle.main(Screen)
    pygame.display.update()
    Clock.tick(60)
