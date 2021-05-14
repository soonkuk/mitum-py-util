import mitum.log as log
import rlp
from mitum.common import Hash, Hint, Int, Text, bconcat
from rlp.sedes import List


class Memo(rlp.Serializable):
    fields = (
        ('m', Text),
    )
    
    def memo(self):
        return self.as_dict()['m'].content()
    
    def to_bytes(self):
        return self.as_dict()['m'].to_bytes()


class Amount(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('big', Int),
        ('cid', Text),
    )

    def to_bytes(self):
        d = self.as_dict()
        big_byte = d['big'].to_bytes()
        cid_byte = d['cid'].to_bytes()

        log.rlog('Amount', log.LOG_TO_BYTES, '')
        return bconcat(big_byte, cid_byte)


class Address(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('addr', Text),
    )

    def hint(self):
        return self.as_dict()['h'].hint

    def hinted(self):
        d = self.as_dict()
        return d['addr'].content() + '-' + d['h'].hint

    def to_bytes(self):
        return self.as_dict()['addr'].to_bytes()

    def to_bytes_hinted(self):
        return self.hinted().encode()


class FactSign(rlp.Serializable):
    fields = (
            ('h', Hint),
            ('signer', Address),
            ('sign', Text),
            ('t', Text),
        )

    def to_bytes(self):
        d = self.as_dict()
        bsigner = d['signer'].to_bytes()
        bsign = d['sign'].to_bytes()
        btime = d['t'].to_bytes()

        return bconcat(bsigner, bsign, btime)


class OperationFactBody(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('token', Text),
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
