import rlp
from rlp.sedes import *


class Target(rlp.Serializable):
    fields = (
        ('text', text),
    )


target = Target('here')

print(target.as_dict())
print(target.as_dict()['text'])
print(target.as_dict()['text'].encode())