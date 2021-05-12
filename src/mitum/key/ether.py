from mitum.key import KeyPair
from mitum.common import Hint
import rlp

# ecdsa

class ETHKeyPair(KeyPair):
    fields = (
        ('h', Hint),
        # ('privkey', text),
        # ('pubkey', text),
    )

    def sign(self, b):
        # hs = sha256 checksum(b)
        # signature = ecdsa sign(hs)
        pass