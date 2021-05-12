import rlp
from rlp.sedes import *


class Target(rlp.Serializable):
    fields = (
        ('text', text),
    )

class ListTarget(rlp.Serializable):
    fields = (
        ('l', List((Target,), False)),
    )


target = []
target.append(Target('tar1'))
target.append(Target('tar2'))
target.append(Target('tar3'))
target.append(Target('tar4'))
target.append(Target('tar5'))

list_target = ListTarget(target)
llist_target = list(list_target)

tar1 = bytearray('a'.encode())
tar2 = bytearray('b'.encode())
tar3 = bytearray('c'.encode())

print(list_target)
print(llist_target)
print(tar1 + tar2 + tar3)