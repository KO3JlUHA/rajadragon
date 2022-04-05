import socket
import sys
import threading
import pygame

e = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 20005)
cords = [120, 120]

pygame.init()
Screen = pygame.display.set_mode((1200, 700))
clock = pygame.time.Clock()


def recv():
    try:
        while 1:
            msg = e.recvfrom(1024)[0].decode()
            x, y = msg.split(',')
            x = int(x)
            y = int(y)
            cords[0] = x
            cords[1] = y

    except KeyboardInterrupt:
        return


def main():
    e.sendto('hi'.encode(), serverAddressPort)

    threading.Thread(target=recv, daemon=True).start()

    while 1:
        keys = pygame.key.get_pressed()
        msg = f'{keys[pygame.K_d] - keys[pygame.K_a]}.{keys[pygame.K_s] - keys[pygame.K_w]}'
        if msg != '0.0':
            print(msg)
            e.sendto(msg.encode(), serverAddressPort)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                e.sendto('!L'.encode(), serverAddressPort)
                pygame.quit()
                sys.exit()
        Screen.fill('white')
        pygame.draw.rect(Screen, (255, 0, 0), ((cords[0], cords[1]), (100, 100)))
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
