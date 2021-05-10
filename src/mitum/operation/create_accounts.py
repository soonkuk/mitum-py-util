from . import *
from ..common import Hint
from ..key import Keys

import rlp
from rlp.sedes import *


# CreateAccountsItem
# variable: h(Hint), amounts(Amount[]), ks(Keys)
class CreateAccountsItem(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('amounts', List(Amount,), False),
        ('ks', Keys),
    )


# CreateAccountsFact
# variable: h(Hint), hs(SHA256), token(str), sender(str), items(CreateAccountsItem[])
class CreateAccountsFact(OperationFact):
    fields = (
        ('h', Hint),
        ('hs', text),
        ('token', text),
        ('sender', text),
        ('items', List(CreateAccountsItem,), False),
    )


# CreateAccounts
# variable: memo(Memo), h(Hint), hs(SHA256), fact(CreateAccountsFact), fact_sg(FactSign[])
class CreateAccounts(Operation):
    fields = (
        ('memo', Memo),
        ('h', Hint),
        ('hs', text),
        ('fact', CreateAccountsFact),
        ('fact_sg', List(FactSign,), False),
    )
