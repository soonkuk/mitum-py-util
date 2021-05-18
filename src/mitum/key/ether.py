from mitum.common import Hint
from mitum.hash import sha
from mitum.constant import VERSION
from mitum.hint import ETHER_PBLCKEY, ETHER_PRIVKEY
from mitum.key.base import KeyPair, BaseKey, to_basekey

import ecdsa

import base64

class ETHKeyPair(KeyPair):
    fields = (
        ('privkey', BaseKey),
        ('pubkey', BaseKey),
    )

    def sign(self, b):
        pk = self.as_dict()['privkey'].key
        sk = ecdsa.SigningKey.from_string(pk)

        return base64.b64encode(sk.sign(sha.sha256(b))).decode()


def new_ether_keypair():
    sk = ecdsa.SigningKey.generate()
    vk = sk.get_verifying_key()
    
    return ETHKeyPair(
        to_basekey(ETHER_PRIVKEY, sk.to_string().decode()),
        to_basekey(ETHER_PBLCKEY, vk.to_string().decode()))

def to_ether_keypair(k):
    sk = ecdsa.SigningKey.from_string(k)
    vk = sk.get_verifying_key()
    
    return ETHKeyPair(
        to_basekey(ETHER_PRIVKEY, sk.to_string().decode()),
        to_basekey(ETHER_PBLCKEY, vk.to_string().decode()))
