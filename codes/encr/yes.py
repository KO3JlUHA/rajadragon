import random
import time


def genKey(len: int):
    key = []
    for i in range(len):
        key.append(random.randint(1, 9))
    k = ''
    for num in key:
        k += str(num)

    # print(k)
    return k


def encript(key, msg):
    msg2 = []#
    for i in range(len(msg)):
        msg2.append(chr(ord(msg[i]) + (i+int(key)) * int(key[i % len(key)])))
    msg3 = ''
    for letter in msg2:
        msg3 += letter
    return msg3


def decript(key, msg):
    msg2 = []
    for i in range(len(msg)):
        msg2.append(chr(ord(msg[i]) - (i+int(key)) * int(key[i % len(key)])))

    msg3 = ''
    for letter in msg2:
        msg3 += letter
    return msg3


key = genKey(5)
print(key)
key = '99999'


msg = input('enter smthg\n')
t = time.time()
sipher = encript(key, msg)
print(sipher)

unsipher = decript(key, sipher)
print(unsipher)
print(time.time()-t)