import base58
from mitum.common import bconcat
from mitum.constant import NETWORK_ID
from mitum.key.ether import to_ether_keypair


EXPECTED_SIGNATURE = "5BpRZ4Gue5cSYNKY1H2joFVUXDU6vqXLo5AhdeFYCc12asSL2wcpbfvv37yo7JJXRbfREfkcgiSX6VfUnuCdtfp6r3xue"

FACT_HASH = "28YF5Y7A1x55MKzwNKRVuCRZEqAEMdLYHSkhpdVY4ZNS"
sk = "0c8f898c2887db97f9648dcf29359cd6ec7a283dcf726450f9d29795abd8787d"
vk = "04b3b30bbc253769998dd30f3a73d44f62f64658c458f25d1a9c42b68e60dc1bbaff869938ecb05fb618ac6a62150382000d55c3ede7512536cfa1cb366f0bb7a4"

signed_at = "2021-05-20T07:23:30.686786252Z"

kp = to_ether_keypair(sk, vk)
signature = kp.sign(bconcat(base58.b58decode(FACT_HASH.encode()), NETWORK_ID.encode()))

result = signature == EXPECTED_SIGNATURE

print("[CHECK] signature: " + str(result))
if not result:
    print("RESULT:   " + signature)
    print("EXPECTED: " + EXPECTED_SIGNATURE)








