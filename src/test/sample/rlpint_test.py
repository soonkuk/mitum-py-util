import rlp
from rlp.sedes import *


class Target(rlp.Serializable):
    fields = (
        ('int', big_endian_int),
    )


target = Target(88)
compare = int(88)

print(compare.bit_length())
print(target.as_dict()['int'].to_bytes(length=1, byteorder='big'))
print(compare.to_bytes(length=1, byteorder='big'))