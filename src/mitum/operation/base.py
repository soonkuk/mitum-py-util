import mitum.log as log
import rlp
from mitum.common import Hash, Hint, Int, bconcat
from rlp.sedes import List, text,binary


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

        log.rlog('Amount', log.LOG_TO_BYTES, '')
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
        # bsign = d['sign'].encode()
        bsign = d['sign']
        btime = d['t'].encode()

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
