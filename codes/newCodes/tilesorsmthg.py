tileSize = 32
tilesPerLine = 18


def calcTopLeft(id: int):
    x = int(id % tilesPerLine)
    x *= tileSize
    y = int(id / tilesPerLine)
    y *= tileSize
    cord = x + (y * tileSize * tilesPerLine)
    print(cord)
    return x, y


def main():
    while 1:
        print(calcTopLeft(int(input('enter id\n'))))


if __name__ == '__main__':
    main()
