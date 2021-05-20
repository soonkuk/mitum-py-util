import mitum.log as log
import rlp
from mitum.common import Hash, Hint, bconcat
from mitum.constant import NETWORK_ID
from mitum.hash import sha
from mitum.key.base import Keys
from mitum.operation import (Address, Amount, FactSign, Memo, Operation,
                             OperationBody, OperationFact, OperationFactBody)
from mitum.operation.base import _newFactSign
from rlp.sedes import List, text


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
        ('token', text),
        ('sender', Address),
        ('items', List((CreateAccountsItem,), False)),
    )

    def to_bytes(self):
        d = self.as_dict()
        items = d['items']

        bitems = bytearray()
        for i in items:
            bitems += bytearray(i.to_bytes())
        
        btoken = d['token'].encode()
        bsender = d['sender'].hinted.encode()
        bitems = bytes(bitems)

        return bconcat(btoken, bsender, bitems)

    def generate_hash(self):
        return sha.sum256(self.to_bytes())


class CreateAccountsFact(OperationFact):
    fields = (
        ('hs', Hash),
        ('body', CreateAccountsFactBody),
    )

    @property
    def hash(self):
        return self.as_dict()['hs']

    def newFactSign(self, priv, pub):
        b = bconcat(self.hash.digest, NETWORK_ID.encode())
        return _newFactSign(b, priv, pub)


class CreateAccountsBody(OperationBody):
    fields = (
        ('memo', Memo),
        ('h', Hint),
        ('fact', CreateAccountsFact),
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


class CreateAccounts(Operation):
    fields = (
        ('hs', Hash),
        ('body', CreateAccountsBody),
    )

    @property
    def hash(self):
        return self.as_dict()['hs']

