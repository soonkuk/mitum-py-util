import hashlib


def sha256(b):
    print('[CALL] sha256(' + str(b) + ')')
    return sum256(b)

def dsha256(b):
    # hashlib sha256 2
    pass

def sum256(b):
    sha3 = hashlib.sha3_256()
    sha3.update(b)
    return sha3.digest()
