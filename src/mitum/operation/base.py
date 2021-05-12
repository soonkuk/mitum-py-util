from mitum.common import bconcat
from mitum.common import Hint, Text, Int

import rlp
from rlp.sedes import *


class Memo(rlp.Serializable):
    fields = (
        ('m', Text),
    )
    
    def memo(self):
        return self.as_dict()['m'].content()
    
    def to_bytes(self):
        return self.as_dict()['m'].to_bytes()


class Amount(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('big', Int),
        ('cid', Text),
    )

    def to_bytes(self):
        d = self.as_dict()
        big_byte = d['big'].to_bytes()
        cid_byte = d['cid'].to_bytes()
        print('[CALL] Amount.to_bytes()')
        return bconcat(big_byte, cid_byte)


class FactSign(rlp.Serializable):
    fields = (
            ('h', Hint),
            ('signer', text),
            ('sign', text),
            ('t', text),
        )


class Address(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('addr', Text),
    )

    def hint(self):
        return self.as_dict()['h'].hint

    def hinted(self):
        d = self.as_dict()
        return d['addr'].content() + '-' + d['h'].hint

    def to_bytes(self):
        return self.as_dict()['addr'].to_bytes()

    def to_bytes_hinted(self):
        return self.hinted().encode()


class OperationFactBody(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('token', Text),
    )

    def to_bytes(self):
        pass

    def generate_hash(self):
        pass

class OperationFact(rlp.Serializable):
    fields = (
        ('hs', text),
        ('body', OperationFactBody),
    )

    def hash(self):
        return self.as_dict()['hs']


class OperationBody(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('fact', OperationFact),
        ('fact_sg', List((FactSign,), False)),
    )

    def generate_hash(self):
        pass

class Operation(rlp.Serializable):
    fields = (
        ('hs', text),
        ('body', OperationBody),
    )

    def hash(self):
        return self.as_dict()['hs']

