from ..common import Hint

import rlp
from rlp.sedes import *


# BaseKey
# variable:
class BaseKeyPair(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('privkey', text),
        ('pubkey', text),
    )

    @classmethod
    def sign(cls):
        pass


# Key
# variable:
class Key(BaseKey):
    fields = (
        ('h', Hint),
        ('k', text),
        ('w', big_endian_int),
    )


# Keys
# variable:
class Keys(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('hs', text),
        ('threshold', big_endian_int),
        ('ks', List(Key,), False),
    )

