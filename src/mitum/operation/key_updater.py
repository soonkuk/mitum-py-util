from . import *
from ..common import Hint
from ..key import Keys

import rlp
from rlp.sedes import *


# KeyUpdaterFact
# variable: h(Hint), hs(SHA256), token(str), target(str), cid(str), ks(Keys)
class KeyUpdaterFact(OperationFact):
    fields = (
        ('h', Hint),
        ('hs', text),
        ('token', text),
        ('target', text),
        ('cid', text),
        ('ks', Keys),
    )
    


# KeyUpdater
# variable: memo(Memo), h(Hint), hs(SHA256), fact(KeyUpdaterFact), fact_sg(FactSign[])
class KeyUpdater(Operation):
    fields = (
        ('memo', Memo),
        ('h', Hint),
        ('hs', text),
        ('fact', KeyUpdaterFact),
        ('fact_sg', List(FactSign,), False),
    )