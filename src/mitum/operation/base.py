import mitum.log as log
import rlp
from mitum.common import (Hash, Hint, Int, bconcat, iso8601TimeStamp,
                          parseAddress, parseISOtoUTC)
from mitum.constant import NETWORK_ID, VERSION
from mitum.hint import (BASE_FACT_SIGN, BTC_PBLCKEY, ETHER_PBLCKEY,
                        STELLAR_PBLCKEY)
from mitum.key.btc import to_btc_keypair
from mitum.key.ether import to_ether_keypair
from mitum.key.stellar import to_stellar_keypair
from rlp.sedes import List, binary, text


class Memo(rlp.Serializable):
    fields = (
        ('m', text),
    )
    
    @property
    def memo(self):
        return self.as_dict()['m']
    
    def to_bytes(self):
        return self.as_dict()['m'].encode()


class Amount(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('big', Int),
        ('cid', text),
    )

    def to_bytes(self):
        d = self.as_dict()
        bbig = d['big'].tight_bytes()
        bcid = d['cid'].encode()

        return bconcat(bbig, bcid)


class Address(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('addr', text),
    )

    @property
    def hint(self):
        return self.as_dict()['h'].hint

    @property
    def hinted(self):
        d = self.as_dict()
        return d['addr'] + '-' + d['h'].hint

    def to_bytes(self):
        return self.as_dict()['addr'].encode()


class FactSign(rlp.Serializable):
    fields = (
            ('h', Hint),
            ('signer', Address),
            ('sign', binary),
            ('t', text),
        )

    def to_bytes(self):
        d = self.as_dict()
        bsigner = d['signer'].hinted.encode()
        bsign = d['sign']
        btime = parseISOtoUTC(d['t']).encode()

        return bconcat(bsigner, bsign, btime)


class OperationFactBody(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('token', text),
    )

    def to_bytes(self):
        pass

    def generate_hash(self):
        pass


class OperationFact(rlp.Serializable):
    fields = (
        ('hs', Hash),
        ('body', OperationFactBody),
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
        if vk.hint.type == BTC_PBLCKEY:
            kp = to_btc_keypair(saddr, vaddr)
            signature = kp.sign(b)
        elif vk.hint.type == ETHER_PBLCKEY:
            kp = to_ether_keypair(saddr, vaddr)
            signature = kp.sign(b)
        elif vk.hint.type == STELLAR_PBLCKEY:
            kp = to_stellar_keypair(saddr, vaddr)
            signature = kp.sign(bconcat(b))

        return FactSign(
            Hint(BASE_FACT_SIGN, VERSION),
            vk,
            signature,
            iso8601TimeStamp(),
        )


class OperationBody(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('fact', OperationFact),
        ('fact_sg', List((FactSign,), False)),
    )

    def generate_hash(self):
        pass


class Operation(rlp.Serializable):
    fields = (
        ('hs', Hash),
        ('body', OperationBody),
    )

    def hash(self):
        return self.as_dict()['hs']
