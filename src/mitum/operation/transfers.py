from . import *
from ..common import Hint
from ..key import Keys

import rlp
from rlp.sedes import *


class TransfersItem(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('receiver', text),
        ('amounts', List(Amount, ), False),
    )


class TransfersFact(OperationFact):
    fields = (
        ('h', Hint),
        ('hs', text),
        ('token', text),
        ('sender', text),
        ('items', List(TransfersItem, ), False),
    )


class TransfersOperation(Operation):
    fields = (
        ('memo', Memo),
        ('h', Hint),
        ('hs', text),
        ('fact', TransfersFact),
        ('fact_sg', List(FactSign,), False),
    )