from . import *
from ..common import Hint, String
from ..common import bconcat
from ..key import Keys
from ..hash import sha

from rlp.sedes import *


class KeyUpdaterFactBody(OperationFactBody):
    fields = (
        ('h', Hint),
        ('token', String),
        ('target', Address),
        ('cid', String),
        ('ks', Keys),
    )
    
    @classmethod
    def to_bytes(cls):
        d = cls.as_dict()

        btoken = d['token'].to_bytes()
        btarget = d['target'].to_bytes_hinted()
        bkeys = d['ks'].to_bytes()
        bcid = d['cid'].to_bytes()
        return bconcat(btoken, btarget, bkeys, bcid)


    @classmethod
    def generate_hash(cls):
        return sha.sha256(cls.to_bytes())
    

class KeyUpdaterFact(OperationFact):
    fields = (
        ('hs', text),
        ('body', KeyUpdaterFactBody),
    )

    @classmethod
    def hash(cls):
        return cls.as_dict()['hs']


class KeyUpdaterBody(OperationBody):
    fields = (
        ('memo', Memo),
        ('h', Hint),
        ('fact', KeyUpdaterFact),
        ('fact_sg', List((FactSign,), False)),
    )

    @classmethod
    def generate_hash(cls):
        pass


class KeyUpdater(Operation):
    fields = (
        ('hs', text),
        ('body', KeyUpdaterBody),
    )

    @classmethod
    def hash(cls):
        return cls.as_dict()['hs']