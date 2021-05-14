from mitum.common import Hint
from mitum.hash import sha
from mitum.hint import BTC_PBLCKEY, BTC_PRIVKEY
from mitum.key.base import BaseKey, KeyPair, to_basekey

from bitcoinutils.setup import setup
from bitcoinutils.keys import PrivateKey, PublicKey
from bitcoinaddress import Wallet

class BTCKeyPair(KeyPair):
    fields = (
        ('privkey', BaseKey),
        ('pubkey', BaseKey),
    )

    def sign(self, b):
        # setup('mainnet')
        
        # wallet = Wallet(self.as_dict()['privkey'].key)
        # privk = PrivateKey(wif=wallet.key.mainnet.wifc)

        # bhash = sha.dsha256(b)

        # signature = privk.sign_message(b, compressed=False)
        # signature
        # return signature
        pass


def new_btc_keypair():
    pass

def to_btc_keypair(k):
    pass