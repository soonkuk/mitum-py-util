import datetime

import base58
import pytz
import rlp
from rlp.sedes import big_endian_int, binary, text

import mitum.log as log


class Int(rlp.Serializable):
    fields = (
        ('int', big_endian_int),
    )
    
    def tight_bytes(self):
        n = abs(self.as_dict()['int'])
        
        result = bytearray()
        while(n):
            result.append(n & 0xff)
            n = n >> 8
        
        return bytes(result[::-1])

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
    def type(self):
        return self.as_dict()['h_type']

    @property
    def hint(self):
        d = self.as_dict()
        return d['h_type'] + ":" + d['h_ver']


class Hash(rlp.Serializable):
    fields = (
        ('hs', binary),
    )

    @property
    def digest(self):
        return self.as_dict()['hs']

    @property
    def hash(self):
        return base58.b58encode(self.as_dict()['hs']).decode()


def iso8601TimeStamp():
    return str(datetime.datetime.now(tz=pytz.utc).isoformat())

def getNewToken():
    return iso8601TimeStamp()

def parseISOtoUTC(t):
    date, at, z = t[:10], t[11:23], t[26:29] + t[30:]
    return date + " " + at + " " + z + " " + "UTC"

def bconcat(*blist):
    concated = bytearray()
    
    for i in blist:
        concated += bytearray(i)
    
    return bytes(concated)

def parseAddress(addr):
    idx = addr.index('-')
    type = addr[idx+1:idx+5]
    return type, addr[:idx]
