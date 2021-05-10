from ..common import Hint

import rlp
from rlp.sedes import *


class KeyPair(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('privkey', text),
        ('pubkey', text),
    )

    @classmethod
    def sign(cls):
        pass


class BaseKey(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('k', text),
    )
    

class Key(BaseKey):
    fields = (
        ('h', Hint),
        ('k', text),
        ('w', big_endian_int),
    )


class Keys(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('hs', text),
        ('threshold', big_endian_int),
        ('ks', List(Key,), False),
    )

