from . import *
from ..common import Hint
from ..key import Keys

import rlp
from rlp.sedes import *


class CreateAccountsItem(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('amounts', List(Amount,), False),
        ('ks', Keys),
    )


class CreateAccountsFact(OperationFact):
    fields = (
        ('h', Hint),
        ('hs', text),
        ('token', text),
        ('sender', text),
        ('items', List(CreateAccountsItem,), False),
    )


class CreateAccounts(Operation):
    fields = (
        ('memo', Memo),
        ('h', Hint),
        ('hs', text),
        ('fact', CreateAccountsFact),
        ('fact_sg', List(FactSign,), False),
    )
