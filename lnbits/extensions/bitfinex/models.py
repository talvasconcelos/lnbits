from typing import NamedTuple


class Connections(NamedTuple):
    id: str
    wallet: str
    currency: str
    bfx_key: str
    bfx_secret: str

    @classmethod
    def from_row(cls, row: Row) -> "Connections":
        return cls(**dict(row))
