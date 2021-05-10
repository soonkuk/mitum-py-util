from . import BaseKeyPair
import rlp

# ecdsa

# ETHKeyPair
class ETHKeyPair(BaseKeyPair):
    fields = (
        ('h', Hint),
        # ('privkey', text),
        # ('pubkey', text),
    )

    @classmethod
    def sign(self, b):
        # hs = sha256 checksum(b)
        # signature = ecdsa sign(hs)
        pass