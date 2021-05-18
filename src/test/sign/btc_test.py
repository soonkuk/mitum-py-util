from mitum.common import bconcat
from mitum.constant import NETWORK_ID
from mitum.key.btc import to_btc_keypair

EXPECTED_SIGNATURE = "381yXZNahRQxzrGMLscyfCxUCp4XNpzDWDPxAfm8nqUwpzKEDxTFR8mFbqTnJVG39vRjrf28hEPKEnoAFXoFh6VAjBJgsJTG"

sk ="L1jPsE8Sjo5QerUHJUZNRqdH1ctxTWzc1ue8Zp2mtpieNwtCKsNZ"
pk ="rd89GxTnMP91bZ1VepbkBrvB77BSQyQbquEVBy2fN1tV"
signed_at = "2021-05-18T02:02:16.067775Z"

kp = to_btc_keypair(sk, pk)
signature = kp.sign(bconcat(b"'\x92\xa6\xbe\x15\xbcG\x9f6Dd\xe8B\xad5\x1d\xd0?\x8a\xd8\xc7B9`X\xb2\xbc\x9c\x8a@\x91-", NETWORK_ID.encode()))

result = signature == EXPECTED_SIGNATURE

print("[CHECK] signature: " + str(result))
if not result:
    print("RESULT:   " + signature)
    print("EXPECTED: " + EXPECTED_SIGNATURE)
