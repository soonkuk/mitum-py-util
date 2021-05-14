import mitum.log as log
import rlp
from mitum.common import Hash, Hint, Text, bconcat
from mitum.hash import sha
from mitum.operation import (Address, Amount, FactSign, Memo, Operation,
                             OperationBody, OperationFact, OperationFactBody)
from rlp.sedes import List


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
        
        log.rlog('TransfersItem', log.LOG_TO_BYTES, '')
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

        log.rlog('TransfersFactBody', log.LOG_TO_BYTES, '')
        return bconcat(btoken, bsender, bitems)

    def generate_hash(self):
        return sha.sha256(self.to_bytes())


class TransfersFact(OperationFact):
    fields = (
        ('hs', Hash),
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

    def to_bytes(self):
        d = self.as_dict()
        bfact_hs = d['fact'].hash().digest()
        bmemo = d['memo'].to_bytes()

        fact_sg = d['fact_sg']
        bfact_sg = bytearray()
        for sg in fact_sg:
            bfact_sg += bytearray(sg.to_bytes())
        bfact_sg = bytes(bfact_sg)

        log.rlog('TransfersBody', log.LOG_TO_BYTES, '')
        return bconcat(bfact_hs, bfact_sg, bmemo)

    def generate_hash(self):
        return sha.sha256(self.to_bytes())


class Transfers(Operation):
    fields = (
        ('hs', Hash),
        ('body', TransfersBody),
    )

    def hash(self):
        return self.as_dict()['hs']

