from typing import NamedTuple
from sqlite3 import Row


class Connection(NamedTuple):
    id: str
    userd: str
    name: str
    wallet: str
    bfx_key: str
    bfx_secret: str
