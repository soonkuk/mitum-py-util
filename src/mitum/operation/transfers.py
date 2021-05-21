import rlp
from mitum.common import Hash, Hint, bconcat
from mitum.hash import sha
from mitum.operation import (Address, Amount, FactSign, Memo, Operation,
                             OperationBody, OperationFact, OperationFactBody)
from mitum.operation.base import _newFactSign
from rlp.sedes import List, text


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
        ('token', text),
        ('sender', Address),
        ('items', List((TransfersItem, ), False)),
    )

    def to_bytes(self):
        d = self.as_dict()
        items = d['items']

        bitems = bytearray()
        for i in items:
            bitems += bytearray(i.to_bytes())

        btoken = d['token'].encode()
        bsender = d['sender'].to_bytes()
        bitems = bytes(bitems)

        return bconcat(btoken, bsender, bitems)

    def generate_hash(self):
        return sha.sum256(self.to_bytes())


class TransfersFact(OperationFact):
    fields = (
        ('hs', Hash),
        ('body', TransfersFactBody),
    )

    @property
    def hash(self):
        return self.as_dict()['hs']

    def newFactSign(self, net_id, priv):
        b = bconcat(self.hash.digest, net_id.encode())
        return _newFactSign(b, priv)


class TransfersBody(OperationBody):
    fields = (
        ('memo', Memo),
        ('h', Hint),
        ('fact', TransfersFact),
        ('fact_sg', List((FactSign,), False)),
    )

    def to_bytes(self):
        d = self.as_dict()
        bfact_hs = d['fact'].hash.digest
        bmemo = d['memo'].to_bytes()

        fact_sg = d['fact_sg']
        bfact_sg = bytearray()
        for sg in fact_sg:
            bfact_sg += bytearray(sg.to_bytes())
        bfact_sg = bytes(bfact_sg)

        return bconcat(bfact_hs, bfact_sg, bmemo)

    def generate_hash(self):
        return sha.sum256(self.to_bytes())


class Transfers(Operation):
    fields = (
        ('hs', Hash),
        ('body', TransfersBody),
    )

    @property
    def hash(self):
        return self.as_dict()['hs']

    def to_dict(self):
        pass
