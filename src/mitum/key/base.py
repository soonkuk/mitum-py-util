import mitum.log as log
import rlp
from mitum.common import Hash, Hint, Int, Text, bconcat
from mitum.hash import sha
from rlp.sedes import List
from mitum.constant import VERSION


class BaseKey(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('k', Text),
    )

    @property
    def key(self):
        return self.as_dict()['k']

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

        log.rlog('Key', log.LOG_TO_BYTES, '')
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

        log.rlog('KeysBody', log.LOG_TO_BYTES, '')
        return bconcat(bkeys, bthreshold)

    def generate_hash(self):
        return sha.sha256(self.to_bytes())


class Keys(rlp.Serializable):
    fields = (
        ('hs', Hash),
        ('body', KeysBody),
    )

    def to_bytes(self):
        return self.as_dict()['body'].to_bytes()

    def hash(self):
        return self.as_dict()['hs']


class KeyPair(rlp.Serializable):
    fields = (
        ('privkey', BaseKey),
        ('pubkey', BaseKey),
    )

    def sign(self):
        pass


def to_basekey(type, k):
    hint = Hint(type, VERSION)
    return BaseKey(hint, k)