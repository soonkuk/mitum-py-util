from . import BaseKeyPair
import rlp

# bitcoinlib
# wif

# BTCKeyPair
class BTCKeyPair(BaseKeyPair):
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