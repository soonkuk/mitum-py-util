from mitum.common import Hint
from mitum.hint import STELLAR_PBLCKEY, STELLAR_PRIVKEY
from mitum.key.base import KeyPair, BaseKey, to_basekey

import stellar_sdk as stellar


class StellarKeyPair(KeyPair):
    fields = (
        ('privkey', BaseKey),
        ('pubkey', BaseKey),
    )

    def sign(self, b):
        kp = stellar.Keypair.from_secret(self.as_dict()['privkey'].key)

        return kp.sign(b).decode()


def new_stellar_keypair():
    kp = stellar.Keypair.random()
    return StellarKeyPair(
        to_basekey(STELLAR_PRIVKEY, kp.secret),
        to_basekey(STELLAR_PBLCKEY, kp.public_key))


def to_stellar_keypair(k):
    kp = stellar.Keypair.from_secret(k)
    return StellarKeyPair(
        to_basekey(STELLAR_PRIVKEY, kp.secret),
        to_basekey(STELLAR_PBLCKEY, kp.public_key))