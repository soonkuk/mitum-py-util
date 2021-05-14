import hashlib

import base58
import mitum.log as log
from mitum.common import Hash


def sha256(b):
    digest = sum256(b)

    log.rlog(
        '', log.LOG_SHA256, b,
        str(base58.b58encode(digest))
    )
    
    return Hash(digest)

def dsha256(b):
    single_digest = sum256(b)
    double_digest = sum256(single_digest)
    
    log.rlog(
        '', log.LOG_DSHA256, b, 
        str(base58.b58encode(single_digest)),
        str(base58.b58encode(double_digest))
    )
    
    return Hash(double_digest)

def sum256(b):
    sha3 = hashlib.sha3_256()
    sha3.update(b)
    return sha3.digest()
