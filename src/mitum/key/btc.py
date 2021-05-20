import hashlib

import base58
import ecdsa
from bitcoinutils.keys import PrivateKey
from bitcoinutils.setup import setup
from ecdsa.curves import SECP256k1
from ecdsa.util import *
from mitum.hash import sha
from mitum.hint import BTC_PBLCKEY, BTC_PRIVKEY
from mitum.key.base import BaseKey, KeyPair, to_basekey


class BTCKeyPair(KeyPair):
    fields = (
        ('privkey', BaseKey),
        ('pubkey', BaseKey),
    )

    def sign(self, b):
        setup('mainnet')
        
        hs = sha.sha256(b).digest
        wif = self.as_dict()['privkey'].key
        
        pk = PrivateKey(wif=wif)
        sk = ecdsa.SigningKey.from_string(pk.key.to_string(), curve=SECP256k1)
        
        signature = sk.sign_deterministic(hs, hashfunc=hashlib.sha256, sigencode=sigencode_der_canonize)
        
        return base58.b58encode(signature).decode()


def to_btc_keypair(priv, pub):
    wif = base58.b58encode_check(base58.b58decode_check(priv)[:-1]).decode()
 
    return BTCKeyPair(
        to_basekey(BTC_PRIVKEY, wif),
        to_basekey(BTC_PBLCKEY, pub)
    )
