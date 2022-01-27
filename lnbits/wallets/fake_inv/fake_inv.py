from binascii import unhexlify
from decimal import Decimal

from pyln.proto.invoice import (
    Invoice,
    RouteHint,
    RouteHintSet,
    bech32_encode,
    bitarray_to_u5,
    bitstring,
    coincurve,
    encode_fallback,
    hashlib,
    shorten_amount,
    tagged,
    tagged_bytes,
)
from pyln.proto.primitives import PrivateKey, Secret


class FakeInvoice(Invoice):
    def __init__(self, *args, **kwargs):
        Invoice.__init__(self, *args, **kwargs)
        self.features = 0

    def encode(self, privkey):
        if self.amount:
            amount = Decimal(str(self.amount))
            # We can only send down to millisatoshi.
            if amount * 10 ** 12 % 10:
                raise ValueError(
                    "Cannot encode {}: too many decimal places".format(self.amount)
                )

            amount = self.currency + shorten_amount(amount)
        else:
            amount = self.currency if self.currency else ""

        hrp = "ln" + amount

        # Start with the timestamp
        data = bitstring.pack("uint:35", self.date)

        # Payment hash
        data += tagged_bytes("p", self.paymenthash)
        tags_set = set()

        if self.route_hints is not None:
            for rh in self.route_hints.route_hints:
                data += tagged_bytes("r", rh.to_bytes())

        if self.features != 0:
            b = "{:x}".format(self.features)
            if len(b) % 2 == 1:
                b = "0" + b
            data += tagged_bytes("9", unhexlify(b))

        for k, v in self.tags:

            # BOLT #11:
            #
            # A writer MUST NOT include more than one `d`, `h`, `n` or `x` fields,
            if k in ("d", "h", "n", "x"):
                if k in tags_set:
                    raise ValueError("Duplicate '{}' tag".format(k))

            if k == "r":
                pubkey, channel, fee, cltv = v
                route = (
                    bitstring.BitArray(pubkey)
                    + bitstring.BitArray(channel)
                    + bitstring.pack("intbe:64", fee)
                    + bitstring.pack("intbe:16", cltv)
                )
                data += tagged("r", route)
            elif k == "f":
                data += encode_fallback(v, self.currency)
            elif k == "d":
                data += tagged_bytes("d", v.encode())
            elif k == "s":
                data += tagged_bytes("s", v)
            elif k == "x":
                # Get minimal length by trimming leading 5 bits at a time.
                expirybits = bitstring.pack("intbe:64", v)[4:64]
                while expirybits.startswith("0b00000"):
                    expirybits = expirybits[5:]
                data += tagged("x", expirybits)
            elif k == "h":
                data += tagged_bytes("h", hashlib.sha256(v.encode("utf-8")).digest())
            elif k == "n":
                data += tagged_bytes("n", v)
            else:
                # FIXME: Support unknown tags?
                raise ValueError("Unknown tag {}".format(k))

            tags_set.add(k)

        # BOLT #11:
        #
        # A writer MUST include either a `d` or `h` field, and MUST NOT include
        # both.
        if "d" in tags_set and "h" in tags_set:
            raise ValueError("Cannot include both 'd' and 'h'")
        if "d" not in tags_set and "h" not in tags_set:
            raise ValueError("Must include either 'd' or 'h'")

        # We actually sign the hrp, then data (padded to 8 bits with zeroes).
        privkey = coincurve.PrivateKey(secret=bytes(unhexlify(privkey)))
        data += privkey.sign_recoverable(
            bytearray([ord(c) for c in hrp]) + data.tobytes()
        )

        return bech32_encode(hrp, bitarray_to_u5(data))
