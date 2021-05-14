import datetime

import base58
import pytz
import rlp
from rlp.sedes import big_endian_int, binary, text

import mitum.log as log


class Text(rlp.Serializable):
    fields = (
        ('content', text),
    )

    def content(self):
        return self.as_dict()['content']

    def to_bytes(self):
        return self.as_dict()['content'].encode()


class Int(rlp.Serializable):
    fields = (
        ('int', big_endian_int),
    )
    
    def to_bytes(self):
        n = self.as_dict()['int']
        count = 0

        result = bytearray()
        while (n):
            result.append(n & 0xff)
            n = n >> 8
            count += 1
        result = bytearray([0]* (8-count)) + result

        return bytes(result[::-1])


class Hint(rlp.Serializable):
    fields = (
        ('h_type', text),
        ('h_ver', text),
    )
    
    @property
    def hint(self):
        d = self.as_dict()
        return d['h_type'] + ":" + d['h_ver']


class Hash(rlp.Serializable):
    fields = (
        ('hs', binary),
    )

    def digest(self):
        return self.as_dict()['hs']

    def hash(self):
        return base58.b58encode(self.as_dict()['hs']).decode()


def iso8601TimeStamp():
    return str(datetime.datetime.now(tz=pytz.utc).isoformat())


def getNewToken():
    return iso8601TimeStamp()


def bconcat(*blist):
    concated = bytearray()
    
    for i in blist:
        concated += bytearray(i)
    
    log.rlog('', log.LOG_BCONCAT, blist, concated, list(concated))
    return bytes(concated)
