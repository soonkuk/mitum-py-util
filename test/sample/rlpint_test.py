import rlp
from rlp.sedes import *


class Target(rlp.Serializable):
    fields = (
        ('int', big_endian_int),
    )


target = Target(1000)
compare = int(1000)

print(target.as_dict()['int'].to_bytes(length=5, byteorder='big'))
print(compare.to_bytes(length=5, byteorder='big'))