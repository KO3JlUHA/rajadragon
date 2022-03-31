import random


def genKey(len: int):
    key = []
    for i in range(len):
        key.append(random.randint(1, 9))
    k = ''
    for num in key:
        k += str(num)

    return k


def encript(key, msg):
    msg2 = []
    toencript = ''
    for i in range(3 - len(str(len(msg)))):
        toencript += '0'
    for letter in str(len(msg)):
        toencript += letter

    toencript += msg
    while len(toencript) < 256:
        toencript += chr(random.randint(ord('a'),ord('z')))

    for i in range(256):
        msg2.append(chr(ord(toencript[i]) + (i + int(key)) * int(key[i % len(key)])))

    msg3 = ''
    for letter in msg2:
        msg3 += letter

    return msg3


def decript(key, msg):
    msg2 = []
    lenn = ''
    for i in range(3):
        lenn += chr(ord(msg[i]) - (i + int(key)) * int(key[i % len(key)]))
    lenn = int(lenn)

    for i in range(3, 3 + lenn):
        msg2.append(chr(ord(msg[i]) - (i + int(key)) * int(key[i % len(key)])))

    msg3 = ''
    for letter in msg2:
        msg3 += letter
    return msg3