from mitum.key import KeyPair
from mitum.common import Hint
import rlp

# stellar sdk

class StellarKeyPair(KeyPair):
    fields = (
        ('h', Hint),
        # ('privkey', text),
        # ('pubkey', text),
    )

    def sign(self, b):
        # sign
        pass

    