from mitum.common import Hint
from mitum.hint import ETHER_PBLCKEY, ETHER_PRIVKEY
from mitum.key.base import KeyPair, BaseKey, to_basekey

class ETHKeyPair(KeyPair):
    fields = (
        ('privkey', BaseKey),
        ('pubkey', BaseKey),
    )

    def sign(self, b):
        # hs = sha256 checksum(b)
        # signature = ecdsa sign(hs)
        pass


def new_ether_keypair():
    pass

def to_ether_keypair(k):
    pass
