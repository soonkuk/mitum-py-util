import hashlib


def sha256(b):
    return sum256(b)

def dsha256(b):
    # hashlib sha256 2
    pass

def sum256(b):
    return hashlib.sha3_256(b).hexdigest()
