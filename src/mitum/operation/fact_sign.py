from ..common import iso8601TimeStamp
from ..common import Hint

import rlp
from rlp.sedes import *

# FactSign
# variable: h(Hint), pbk(bytes), sg(bytes), t(str)
class FactSign(rlp.Serializable):
    fields = (
            ('h', Hint),
            ('signer', text),
            ('sign', text),
            ('t', text),
        )

