from ..common import Hint, String, Int
from ..common import bconcat
from ..hash import sha

import rlp
from rlp.sedes import *


class KeyPair(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('privkey', String),
        ('pubkey', String),
    )

    @classmethod
    def sign(cls):
        pass


class BaseKey(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('k', String),
    )
    

class Key(BaseKey):
    fields = (
        ('h', Hint),
        ('k', String),
        ('w', Int),
    )

    def hinted(self):
        return self.as_dict()['k'].content() + "-" + self.as_dict()['h'].hint

    def to_bytes(self):
        bkey = self.hinted().encode()
        bweight = self.as_dict()['w'].to_bytes()
        return bconcat(bkey, bweight)


class KeysBody(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('threshold', Int),
        ('ks', List((Key,), False)),
    )

    def to_bytes(self):
        d = self.as_dict()
        keys = d['ks']

        lkeys = list(keys)
        lkeys.sort(key=lambda x: x.to_bytes())

        bkeys = bytearray()
        for k in lkeys:
            bkeys += k.to_bytes()

        bkeys = bytes(bkeys)
        bthreshold = d['threshold'].to_bytes()
        return bconcat(bkeys, bthreshold)

    def generate_hash(self):
        return sha.sha256(self.to_bytes())


class Keys(rlp.Serializable):
    fields = (
        ('hs', text),
        ('body', KeysBody),
    )

    def to_bytes(self):
        return self.as_dict()['body'].to_bytes()