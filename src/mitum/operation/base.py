from ..common import getNewToken
from ..common import Hint
from ..constant import VERSION
from . import FactSign

import rlp
from rlp.sedes import *


# Memo
# variable: content(str)
class Memo(rlp.Serializable):
    fields = (
        ('m', text),
    )
    
    def memo(self):
        return self.as_dict()['m']
    
    def to_bytes(self):
        return memo().encode()


# OperationFact
# variable: h(Hint), hs(SHA256), token(bytes)
class OperationFact(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('hs', text),
        ('token', text),
    )


# Operation
# variable: h(hint), hs(SHA256), fact(OperationFact), fact_sg(FactSign[])
class Operation(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('hs', text),
        ('fact', OperationFact),
        ('fact_sg', List(FactSign,), False),
    )

