import socket
import rsa

UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
localIP = "0.0.0.0"
localPort = 20003
UDPServerSocket.bind((localIP, localPort))


def generate_keys():
    (pubKey, privKey) = rsa.newkeys(1024)
    return pubKey, privKey


# def load_keys():
#     with open('keys/pubkey.pem.pem', 'rb') as f:
#         pubKey = rsa.PublicKey.load_pkcs1(f.read())
#
#     with open('keys/privkey.pem', 'rb') as f:
#         privKey = rsa.PrivateKey.load_pkcs1(f.read())
#
#     return pubKey, privKey

def encrypt(msg, key):
    return rsa.encrypt(msg.encode('ascii'), key)


def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode('ascii')
    except:
        return False


def sign_sha1(msg, key):
    return rsa.sign(msg.encode('ascii'), key, 'SHA-1')


def verify_sha1(msg, signature, key):
    try:
        return rsa.verify(msg.encode('ascii'), signature, key) == 'SHA-1'
    except:
        return False


pub, priv = generate_keys()
ip = UDPServerSocket.recvfrom(1024)[1]
# print(pub)
UDPServerSocket.sendto(f'{pub.n}${pub.e}'.encode(), ip)

msg = UDPServerSocket.recvfrom(1024)[0]
print(msg)
msg = decrypt(msg, priv)
print(msg)
if msg:
    signature = sign_sha1(msg, priv)

    if verify_sha1(msg, signature, pub):
        print('Signature verified!')