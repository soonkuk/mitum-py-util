from . import *
from ..common import Hint, String
from ..common import bconcat
from ..hash import sha

import rlp
from rlp.sedes import *


class TransfersItem(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('receiver', Address),
        ('amounts', List((Amount, ), False)),
    )

    def to_bytes(self):
        d = self.as_dict()
        amounts = d['amounts']

        bamounts = bytearray()
        for amount in amounts:
            bamounts += bytearray(amount.to_bytes())

        breceiver = d['receiver'].to_bytes()
        bamounts = bytes(bamounts)
        return bconcat(breceiver, bamounts)


class TransfersFactBody(OperationFactBody):
    fields = (
        ('h', Hint),
        ('token', String),
        ('sender', Address),
        ('items', List((TransfersItem, ), False)),
    )
    
    @classmethod
    def to_bytes(cls):
        d = cls.as_dict()
        items = d['items']

        bitems = bytearray()
        for i in items:
            bitems += bytearray(i.to_bytes())

        btoken = d['token'].to_bytes()
        bsender = d['sender'].to_bytes()
        bitems = bytes(bitems)
        return bconcat(btoken, bsender, bitems)


    @classmethod
    def generate_hash(cls):
        return sha.sha256(cls.to_bytes())


class TransfersFact(OperationFact):
    fields = (
        ('hs', text),
        ('body', TransfersFactBody),
    )

    @classmethod
    def hash(cls):
        return cls.as_dict()['hs']


class TransfersBody(OperationBody):
    fields = (
        ('memo', Memo),
        ('h', Hint),
        ('fact', TransfersFact),
        ('fact_sg', List((FactSign,), False)),
    )

    @classmethod
    def generate_hash(cls):
        pass


class Transfers(Operation):
    fields = (
        ('hs', text),
        ('body', TransfersBody),
    )

    @classmethod
    def hash(cls):
        return cls.as_dict()['hs']

