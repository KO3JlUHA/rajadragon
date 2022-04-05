import socket
import threading
from threading import Thread
import queue

e = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
e.bind(('0.0.0.0', 20005))
cords = []
ips = []


def handle_income():
    try:
        while 1:
            msg, ip = e.recvfrom(1024)
            if msg.decode() == 'hi' and ip not in ips:
                ips.append(ip)
                cords.append([120, 120])
            elif msg.decode() == '!L':
                cords.remove(cords[ips.index(ip)])
                ips.remove(ip)
                return
            else:
                x, y = msg.decode().split('.')
                x = 8 * int(x)
                y = 8 * int(y)
                cords[ips.index(ip)][0] += x
                cords[ips.index(ip)][1] += y
                st = str(cords[ips.index(ip)])
                st = st.replace(' ', '')
                st = st.replace('[', '')
                st = st.replace(']', '')
                e.sendto(st.encode(), ip)
    except KeyboardInterrupt:
        return


def main():
    len2 = 0
    Thread(target=handle_income).start()
    while 1:
        print(threading.active_count()-1, len(ips))
        if len2 < len(ips):
            len2 = len(ips)
            for i in range(len2, len(ips)+1):
                Thread(target=handle_income).start()
        elif len2>len(ips):
            len2 = len(ips)


if __name__ == '__main__':
    main()
