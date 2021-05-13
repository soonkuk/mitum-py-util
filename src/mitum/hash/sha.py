import mitum.log as log
import base58
import hashlib

def sha256(b):
    digest = sum256(b)
    log.rlog('', log.LOG_SHA256, b, str(base58.b58encode(digest)))
    return sum256(b)

def dsha256(b):
    # hashlib sha256 2
    pass

def sum256(b):
    sha3 = hashlib.sha3_256()
    sha3.update(b)
    return sha3.digest()
