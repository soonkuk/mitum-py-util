from mitum.common import Hint, Int
from mitum.key.base import Key, Keys, KeysBody, to_basekey
from mitum.hint import *
from mitum.constant import VERSION


EXPECTED_KEYS_HASH = "HhgmNZQvabSfGSyKmXqQfTSJimjPTxsQ31B4Wd1UzFD5"

k = "hayB9VYA5KREe97duDwhtqvGgbRRzL4Y42y5WwrBZADB"
weight = 100
threshold = 100
currency = "MCC"

key = Key(
    Hint(BTC_PBLCKEY, VERSION),
    to_basekey(BTC_PBLCKEY, k),
    Int(weight),
)

key_list = list()
key_list.append(key)

keys_body = KeysBody(
    Hint(MC_KEYS, VERSION),
    Int(threshold),
    key_list,
)

keys = Keys(
    keys_body.generate_hash(),
    keys_body,
)

print("[CHECK] KEYS HASH: " + str(keys.hash.hash == EXPECTED_KEYS_HASH))
print("[CHECK] FACT HASH: ")
print("[CHECK] Operation HASH:" )