from . import *
from ..common import Hint
from ..key import Keys

import rlp
from rlp.sedes import *


class KeyUpdaterFact(OperationFact):
    fields = (
        ('h', Hint),
        ('hs', text),
        ('token', text),
        ('target', text),
        ('cid', text),
        ('ks', Keys),
    )
    

class KeyUpdater(Operation):
    fields = (
        ('memo', Memo),
        ('h', Hint),
        ('hs', text),
        ('fact', KeyUpdaterFact),
        ('fact_sg', List(FactSign,), False),
    )