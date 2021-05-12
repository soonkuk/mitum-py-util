from mitum.key import KeyPair
from mitum.common import Hint
import rlp

# bitcoinlib
# wif

class BTCKeyPair(KeyPair):
    fields = (
        ('h', Hint),
        # ('privkey', text),
        # ('pubkey', text),
    )

    def sign(self, b):
        # hs = double sha256 hash
        # signature = ecdsa(hs)
        pass