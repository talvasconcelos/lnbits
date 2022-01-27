from binascii import unhexlify
from typing import AsyncGenerator, Optional

from ecdsa import SECP256k1, SigningKey

from .base import (
    InvoiceResponse,
    PaymentResponse,
    PaymentStatus,
    StatusResponse,
    Unsupported,
    Wallet,
)


class FakeWallet(Wallet):
    def __init__(self):
        # Something we don't have a preimage for, and allows downstream nodes
        # to recognize this as a test payment.
        PAYMENT_HASH = b"AA" * 32

        # The private key used for the final hop. Well-known so the
        # penultimate hop can decode the onion.
        PRIVKEY = PrivateKey(b"\xAA" * 32)
        PUBKEY = PRIVKEY.public_key()

        sk = SigningKey.generate(curve=SECP256k1)
        self.private_key = sk.to_string().hex()
        print(self.private_key, sk)

    async def create_invoice(
        self,
        amount: int,
        memo: Optional[str] = None,
        description_hash: Optional[bytes] = None,
    ) -> InvoiceResponse:
        #RHASH=unhexlify(b"AA" * 32)
        RHASH=unhexlify('0001020304050607080900010203040506070809000102030405060708090102')
        r = lnencode(LnAddr(RHASH, amount=amount, tags=[('d', '')]), self.private_key)

        checking_id, payment_request, error_message = (
            None,
            None,
            None,
        )
        print(r)
        data = r.json()
        checking_id, payment_request = data["checking_id"], data["payment_request"]
        print(InvoiceResponse(checking_id, payment_request, error_message))
        return InvoiceResponse(checking_id, payment_request, error_message)

    async def status(self) -> StatusResponse:
        print("This backend does nothing, it is here just as a placeholder, you must configure an actual backend before being able to do anything useful with LNbits.")
        return StatusResponse(
            None,
            0,
        )

    async def pay_invoice(self, bolt11: str) -> PaymentResponse:
        raise Unsupported("")

    async def get_invoice_status(self, checking_id: str) -> PaymentStatus:
        raise Unsupported("")

    async def get_payment_status(self, checking_id: str) -> PaymentStatus:
        raise Unsupported("")

    async def paid_invoices_stream(self) -> AsyncGenerator[str, None]:
        yield ""
