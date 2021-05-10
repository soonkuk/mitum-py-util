from ..common import getNewToken
from ..common import Hint
from ..constant import VERSION

import rlp
from rlp.sedes import *


class Memo(rlp.Serializable):
    fields = (
        ('m', text),
    )
    
    def memo(self):
        return self.as_dict()['m']
    
    def to_bytes(self):
        return memo().encode()


class FactSign(rlp.Serializable):
    fields = (
            ('h', Hint),
            ('signer', text),
            ('sign', text),
            ('t', text),
        )


class OperationFact(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('hs', text),
        ('token', text),
    )


class Operation(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('hs', text),
        ('fact', OperationFact),
        ('fact_sg', List(FactSign,), False),
    )

