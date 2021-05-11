from . import *
from ..common import Hint, String
from ..common import bconcat
from ..key import Keys
from ..hash import sha

import rlp
from rlp.sedes import *


class CreateAccountsItem(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('ks', Keys),
        ('amounts', List((Amount,), False)),
    )

    def to_bytes(self):
        d = self.as_dict()
        amounts = d['amounts']

        bamounts = bytearray()
        for amount in amounts:
            bamounts += bytearray(amount.to_bytes())

        bkeys = d['ks'].to_bytes()
        bamounts = bytes(bamounts)
        return bconcat(bkeys, bamounts)


class CreateAccountsFactBody(OperationFactBody):
    fields = (
        ('h', Hint),
        ('token', String),
        ('sender', Address),
        ('items', List((CreateAccountsItem,), False)),
    )

    @classmethod
    def to_bytes(cls):
        d = cls.as_dict()
        items = d['items']

        bitems = bytearray()
        for i in items:
            bitems += bytearray(i.to_bytes())
        
        btoken = d['token'].to_bytes()
        bsender = d['sender'].to_bytes_hinted()
        bitems = bytes(bitems)
        return bconcat(btoken, bsender, bitems)

    @classmethod
    def generate_hash(cls):
        return sha.sha256(cls.to_bytes())


class CreateAccountsFact(OperationFact):
    fields = (
        ('hs', text),
        ('body', CreateAccountsFactBody),
    )

    @classmethod
    def hash(cls):
        return cls.as_dict()['hs']


class CreateAccountsBody(OperationBody):
    fields = (
        ('memo', Memo),
        ('h', Hint),
        ('fact', CreateAccountsFact),
        ('fact_sg', List((FactSign,), False)),
    )

    @classmethod
    def generate_hash(cls):
        pass


class CreateAccounts(Operation):
    fields = (
        ('hs', text),
        ('body', CreateAccountsBody),
    )

    @classmethod
    def hash(cls):
        return cls.as_dict()['hs']

