import mitum.log as log
from mitum.common import Hash, Hint, bconcat
from mitum.hash import sha
from mitum.key.base import Keys
from mitum.operation import (Address, FactSign, Memo, Operation, OperationBody,
                             OperationFact, OperationFactBody)
from rlp.sedes import List, text


class KeyUpdaterFactBody(OperationFactBody):
    fields = (
        ('h', Hint),
        ('token', text),
        ('target', Address),
        ('cid', text),
        ('ks', Keys),
    )
    
    def to_bytes(self):
        d = self.as_dict(self)

        btoken = d['token'].encode()
        btarget = d['target'].hinted.encode()
        bkeys = d['ks'].to_bytes()
        bcid = d['cid'].encode()
      
        log.rlog('KeyUpdaterFactBody', log.LOG_TO_BYTES, '')
        return bconcat(btoken, btarget, bkeys, bcid)


    def generate_hash(self):
        return sha.sha256(self.to_bytes())
    

class KeyUpdaterFact(OperationFact):
    fields = (
        ('hs', Hash),
        ('body', KeyUpdaterFactBody),
    )

    @property
    def hash(self):
        return self.as_dict(self)['hs']


class KeyUpdaterBody(OperationBody):
    fields = (
        ('memo', Memo),
        ('h', Hint),
        ('fact', KeyUpdaterFact),
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

        log.rlog('KeyUpdaterBody', log.LOG_TO_BYTES, '')
        return bconcat(bfact_hs, bfact_sg, bmemo)

    def generate_hash(self):
        return sha.sha256(self.to_bytes())


class KeyUpdater(Operation):
    fields = (
        ('hs', Hash),
        ('body', KeyUpdaterBody),
    )

    @property
    def hash(self):
        return self.as_dict()['hs']
