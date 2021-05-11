from . import KeyPair
from ..operation import Hint
import rlp

# stellar sdk

class StellarKeyPair(KeyPair):
    fields = (
        ('h', Hint),
        # ('privkey', text),
        # ('pubkey', text),
    )

    @classmethod
    def sign(self, b):
        # sign
        pass

    