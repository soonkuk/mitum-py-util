import rlp
from mitum.common import Hash, Hint, bconcat
from mitum.hash import sha
import json
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

    def to_dict(self):
        d = self.as_dict()
        item = {}
        item['_hint'] = d['h'].hint
        item['keys'] = d['ks'].to_dict()
        
        _amounts = d['amounts']
        amounts = list()
        for _amount in _amounts:
            amounts.append(_amount.to_dict())
        item['amounts'] = amounts

        return item

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
        bsender = d['sender'].hinted().encode()
        bitems = bytes(bitems)

        return bconcat(btoken, bsender, bitems)

    def generate_hash(self):
        return sha.sum256(self.to_bytes())


class CreateAccountsFact(OperationFact):
    fields = (
        ('hs', Hash),
        ('body', CreateAccountsFactBody),
    )

    def hash(self):
        return self.as_dict()['hs']

    def newFactSign(self, net_id, priv):
        b = bconcat(self.hash().digest, net_id.encode())
        return _newFactSign(b, priv)

    def to_dict(self):
        d = self.as_dict()['body'].as_dict()
        fact = {}
        fact['_hint'] = d['h'].hint
        fact['hash'] = self.hash().hash
        fact['token'] = d['token']
        fact['sender'] = d['sender'].hinted()

        _items = d['items']
        items = list()
        for item in _items:
            items.append(item.to_dict())
        fact['items'] = items
        return fact


class CreateAccountsBody(OperationBody):
    fields = (
        ('memo', Memo),
        ('h', Hint),
        ('fact', CreateAccountsFact),
        ('fact_sg', List((FactSign,), False)),
    )

    def to_bytes(self):
        d = self.as_dict()
        bfact_hs = d['fact'].hash().digest
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

    def hash(self):
        return self.as_dict()['hs']

    def to_dict(self):
        d = self.as_dict()['body'].as_dict()
        oper = {}
        oper['memo'] = d['memo'].memo
        oper['hint'] = d['h'].hint
        oper['fact'] = d['fact'].to_dict()

        fact_signs = list()
        _sgs = d['fact_sg']
        for _sg in _sgs:
            fact_signs.append(_sg.to_dict())
        oper['fact_signs'] = fact_signs

        return oper

    def to_json(self, file_name):
        with open(file_name, "w") as fp:
            json.dump(self.to_dict(), fp)