from mitum.common import Int
import base58, base64
import mitum.hash.sha as sha
from eth_keys import keys
from eth_account import Account, messages
from mitum.hint import ETHER_PBLCKEY, ETHER_PRIVKEY
from mitum.key.base import BaseKey, KeyPair, to_basekey


class ETHKeyPair(KeyPair):
    fields = (
        ('privkey', BaseKey),
        ('pubkey', BaseKey),
    )

    def sign(self, b):
        pk = keys.PrivateKey(bytes(bytearray.fromhex(self.as_dict()['privkey'].key)))

        b = sha.sha256(b).digest

        signed = pk.sign_msg_hash(b)
        r, s = Int(signed.r), Int(signed.s)

        rlen = Int(len(r.tight_bytes()))
        brlen = rlen.little4_to_bytes()

        signature = bytes(
            bytearray(brlen) + bytearray(r.tight_bytes()) + bytearray(s.tight_bytes())
        )

        return base58.b58encode(signature).decode()


def to_ether_keypair(priv, pub):
    return ETHKeyPair(
        to_basekey(ETHER_PRIVKEY, priv),
        to_basekey(ETHER_PBLCKEY, pub),
    )
