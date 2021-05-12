from mitum.operation import Memo, FactSign, Address
from mitum.operation import OperationBody, Operation
from mitum.operation import OperationFactBody, OperationFact
from mitum.common import Hint, Text
from mitum.common import bconcat
from mitum.key.base import Keys
from mitum.hash import sha

from rlp.sedes import *


class KeyUpdaterFactBody(OperationFactBody):
    fields = (
        ('h', Hint),
        ('token', Text),
        ('target', Address),
        ('cid', Text),
        ('ks', Keys),
    )
    
    def to_bytes(self):
        d = self.as_dict(self)

        btoken = d['token'].to_bytes()
        btarget = d['target'].to_bytes_hinted()
        bkeys = d['ks'].to_bytes()
        bcid = d['cid'].to_bytes()
        print('[CALL] KeyUpdaterFactBoey.to_bytes()')
        return bconcat(btoken, btarget, bkeys, bcid)


    def generate_hash(self):
        return sha.sha256(self.to_bytes())
    

class KeyUpdaterFact(OperationFact):
    fields = (
        ('hs', text),
        ('body', KeyUpdaterFactBody),
    )

    def hash(self):
        return self.as_dict(self)['hs']


class KeyUpdaterBody(OperationBody):
    fields = (
        ('memo', Memo),
        ('h', Hint),
        ('fact', KeyUpdaterFact),
        ('fact_sg', List((FactSign,), False)),
    )

    def generate_hash(self):
        pass


class KeyUpdater(Operation):
    fields = (
        ('hs', text),
        ('body', KeyUpdaterBody),
    )

    def hash(self):
        return self.as_dict()['hs']