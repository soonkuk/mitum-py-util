from mitum.common import Hint, Text, Int
from mitum.common import bconcat
from mitum.hash import sha

import rlp
from rlp.sedes import *


class KeyPair(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('privkey', Text),
        ('pubkey', Text),
    )

    def sign(self):
        pass


class BaseKey(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('k', Text),
    )

    def to_bytes(self):
        return self.as_dict()['k'].encode()

    def hinted(self):
        return self.as_dict()['k'] + "-" + self.as_dict()['h'].hint
    

class Key(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('k', BaseKey),
        ('w', Int),
    )

    def key_bytes(self):
        return self.as_dict()['k'].to_bytes()

    def to_bytes(self):
        d = self.as_dict()
        bkey = d['k'].hinted().encode()
        bweight = self.as_dict()['w'].to_bytes()
        print('[CALL] Key.to_bytes()')
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
        lkeys.sort(key=lambda x: x.key_bytes())

        bkeys = bytearray()
        for k in lkeys:
            bkeys += k.to_bytes()

        bkeys = bytes(bkeys)
        bthreshold = d['threshold'].to_bytes()
        print('[CALL] KeysBody.to_bytes()')
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

    def hash(self):
        return self.as_dict()['hs']