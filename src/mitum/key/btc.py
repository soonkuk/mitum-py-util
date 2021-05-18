import base58
import base64
import ecdsa

from bitcoinutils.keys import PrivateKey
from bitcoinutils.setup import setup
from ecdsa.curves import SECP256k1
from ecdsa.util import sigdecode_der

from mitum.common import Hint
from mitum.constant import VERSION
from mitum.hash import sha
from mitum.hint import BTC_PBLCKEY, BTC_PRIVKEY
from mitum.key.base import BaseKey, KeyPair, to_basekey


class BTCKeyPair(KeyPair):
    fields = (
        ('privkey', BaseKey),
        ('pubkey', BaseKey),
    )

    def sign(self, b):
        hs = sha.dsha256(b)
        wif = self.as_dict()['privkey'].key
        pk = PrivateKey(wif=wif)
        sk = ecdsa.SigningKey.from_string(pk.key.to_string(), curve=SECP256k1)
        signature = sk.sign(b, sigencode=sigdecode_der)
        return base64.b64encode(signature).decode()


def new_btc_keypair():
    pass

def to_btc_keypair(privk, pubk):
    wif = base58.b58encode_check(base58.b58decode_check(privk)[:-1]).decode()
 
    return BTCKeyPair(
        to_basekey(BTC_PRIVKEY, wif),
        to_basekey(BTC_PBLCKEY, pubk)
    )