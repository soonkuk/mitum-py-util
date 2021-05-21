import hashlib

from mitum.common import Hash


def sha256(b):
    sha2 = hashlib.sha256()
    sha2.update(b)
    return Hash(sha2.digest())


def sum256(b):
    sha3 = hashlib.sha3_256()
    sha3.update(b)
    return Hash(sha3.digest())
