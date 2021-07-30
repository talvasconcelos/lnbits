from typing import NamedTuple
from sqlite3 import Row


class Connection(NamedTuple):
    id: str
    user: str
    name: str
    wallet: str
    bfx_key: str
    bfx_secret: str

    @classmethod
    def from_row(cls, row: Row) -> "Connection":
        return cls(**dict(row))
