from mitum.operation import Memo, FactSign, Amount, Address
from mitum.operation import OperationBody, Operation
from mitum.operation import OperationFactBody, OperationFact
from mitum.common import Hint, Text
from mitum.common import bconcat
from mitum.hash import sha

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
        print('[CALL] TransfersItem.to_bytes()')
        return bconcat(breceiver, bamounts)


class TransfersFactBody(OperationFactBody):
    fields = (
        ('h', Hint),
        ('token', Text),
        ('sender', Address),
        ('items', List((TransfersItem, ), False)),
    )

    def to_bytes(self):
        d = self.as_dict()
        items = d['items']

        bitems = bytearray()
        for i in items:
            bitems += bytearray(i.to_bytes())

        btoken = d['token'].to_bytes()
        bsender = d['sender'].to_bytes()
        bitems = bytes(bitems)
        return bconcat(btoken, bsender, bitems)

    def generate_hash(self):
        return sha.sha256(self.to_bytes())


class TransfersFact(OperationFact):
    fields = (
        ('hs', text),
        ('body', TransfersFactBody),
    )

    def hash(self):
        return self.as_dict()['hs']


class TransfersBody(OperationBody):
    fields = (
        ('memo', Memo),
        ('h', Hint),
        ('fact', TransfersFact),
        ('fact_sg', List((FactSign,), False)),
    )

    def generate_hash(self):
        pass


class Transfers(Operation):
    fields = (
        ('hs', text),
        ('body', TransfersBody),
    )

    def hash(self):
        return self.as_dict()['hs']

