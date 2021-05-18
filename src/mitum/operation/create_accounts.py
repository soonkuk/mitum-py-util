import mitum.log as log
import rlp
from mitum.common import Hash, Hint, bconcat, iso8601TimeStamp, parseAddress
from mitum.constant import NETWORK_ID, VERSION
from mitum.hash import sha
from mitum.hint import (BASE_FACT_SIGN, BTC_PBLCKEY, ETHER_PBLCKEY,
                        STELLAR_PBLCKEY)
from mitum.key.base import Keys
from mitum.key.btc import to_btc_keypair
from mitum.key.ether import to_ether_keypair
from mitum.key.stellar import to_stellar_keypair
from mitum.operation import (Address, Amount, FactSign, Memo, Operation,
                             OperationBody, OperationFact, OperationFactBody)
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
        stype, saddr = parseAddress(priv)
        sk = Address(Hint(stype, VERSION), saddr)

        vtype, vaddr = parseAddress(pub)
        vk = Address(Hint(vtype, VERSION), vaddr)
        
        signature = None

        b = bconcat(self.hash.digest, NETWORK_ID.encode())
        if vtype == BTC_PBLCKEY:
            kp = to_btc_keypair(saddr, vaddr)
            signature = kp.sign(b)
        elif vtype == ETHER_PBLCKEY:
            kp = to_ether_keypair(saddr, vaddr)
            signature = kp.sign(b)
        elif vtype == STELLAR_PBLCKEY:
            kp = to_stellar_keypair(saddr, vaddr)
            signature = kp.sign(bconcat(b))

        return FactSign(
            Hint(BASE_FACT_SIGN, VERSION),
            vk,
            signature,
            iso8601TimeStamp(),
        )


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
        # bfact_hs = d['fact'].hash.hash.encode()
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

