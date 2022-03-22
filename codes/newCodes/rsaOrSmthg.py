import rsa
import socket


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


serverAddressPort = ("127.0.0.1", 20003)
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# pubKey, privKey = generate_keys()
# print(type(pubKey))
# print(pubKey)
# message = input('Enter a message:\n')
#
#
#
# ciphertext = encrypt(message, pubKey)
# signature = sign_sha1(message, privKey)
# plaintext = decrypt(ciphertext, privKey)

UDPClientSocket.sendto('wtf'.encode(), serverAddressPort)

keyss = UDPClientSocket.recvfrom(1024)[0].decode()
n, e = keyss.split('$')
n = int(n)
e = int(e)

key2 = rsa.key.PublicKey(e=e, n=n)

message = input('Enter a message:\n')

ciphertext = encrypt(message, key2)
UDPClientSocket.sendto(ciphertext, serverAddressPort)

# print(f'Cipher text: {ciphertext}')
# print(f'Signature: {signature}')
#
# if plaintext:
#     print(f'Plain text: {plaintext}')
# else:
#     print('Could not decrypt the message.')
#
# if verify_sha1(plaintext, signature, pubKey):
#     print('Signature verified!')
# else:
#     print('Could not verify the message signature.')
