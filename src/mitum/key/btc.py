from . import KeyPair
from ..operation import Hint
import rlp

# bitcoinlib
# wif

class BTCKeyPair(KeyPair):
    fields = (
        ('h', Hint),
        # ('privkey', text),
        # ('pubkey', text),
    )

    @classmethod
    def sign(self, b):
        # hs = double sha256 hash
        # signature = ecdsa(hs)
        pass