import secrets
from binascii import hexlify, unhexlify
from random import random
from uuid import uuid4

from ecdsa import SECP256k1, SigningKey, VerifyingKey

RHASH=unhexlify('0001020304050607080900010203040506070809000102030405060708090102')
print(RHASH)
print(secrets.token_hex())

# sk = SigningKey.generate(curve=SECP256k1)
# sk_string = sk.to_string()
# sk2 = SigningKey.from_string(sk_string, curve=SECP256k1)

# privkey = "a65819c459955db11c62d24fa95ca4baa0bb75d3c81bb88fd4368a72f5cdf38d"
# privkey = SigningKey.from_string(bytes(unhexlify(privkey)), curve=SECP256k1)
# # privkey = secp256k1.PrivateKey(bytes(unhexlify(privkey)))
# sig = privkey.sign_digest_deterministic(b"hello world")
# # sig = privkey.ecdsa_sign_recoverable(bytearray([ord(c) for c in hrp]) + data.tobytes())
# # This doesn't actually serialize, but returns a pair of values :(
# print(sig[0], sig[1])
# print(bytes(sig[0]), bytes(sig[1]))

# #print(sk_string.hex())
# #print(sk2.to_string().hex())
