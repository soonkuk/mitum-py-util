from . import BaseKeyPair
import rlp

# stellar sdk

# StellarKeyPair
class StellarKeyPair(BaseKeyPair):
    fields = (
        ('h', Hint),
        # ('privkey', text),
        # ('pubkey', text),
    )

    @classmethod
    def sign(self, b):
        # sign
        pass