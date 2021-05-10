from . import KeyPair
import rlp

# ecdsa

class ETHKeyPair(KeyPair):
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