import datetime
import pytz

import rlp
from rlp.sedes import big_endian_int, text


class String(rlp.Serializable):
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
        blen = self.byte_length()
        return n.to_bytes(length=blen, byteorder='big')

    def byte_length(self):
        return (self.as_dict()['int'].bit_length() + 7) // 8


class Hint(rlp.Serializable):
    fields = (
        ('h_type', text),
        ('h_ver', text),
    )
    
    @property
    def hint(self):
        d = self.as_dict()
        return d['h_type'] + ":" + d['h_ver']


def iso8601TimeStamp():
    return str(datetime.datetime.now(tz=pytz.utc).isoformat())


def getNewToken():
    return iso8601TimeStamp()


def bconcat(*blist):
    concated = bytearray()
    
    for i in blist:
        concated += bytearray(i)
    
    return bytes(concated)