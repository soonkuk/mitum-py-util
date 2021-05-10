from ..common import Hint

# Amount
# variable: h(Hint), amount(int), cid(str)
class Amount(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('amount', big_endian_int),
        ('cid', text),
    )
