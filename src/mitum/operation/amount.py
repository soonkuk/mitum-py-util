from ..common import Hint


class Amount(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('amount', big_endian_int),
        ('cid', text),
    )
