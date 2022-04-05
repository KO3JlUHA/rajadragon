import rsa
def generate_keys():
    (pubKey, privKey) = rsa.newkeys(1024)
    return pubKey, privKey

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