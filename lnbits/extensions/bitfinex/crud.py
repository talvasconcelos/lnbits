from typing import List, Optional

from . import db
from .models import Connection

async def add_bfx_conn(
    user: str,
    wallet: str,
    bfx_key: str,
    bfx_secret: str,
) -> Optional[Connection]:
    result = await db.execute(
        """
        INSERT INTO bitfinex.connections (user, wallet, bfx_key, bfx_secret)
        VALUES (?, ?, ?, ?)
        """,
        (user, wallet, bfx_key, bfx_secret),
    )
    return result

async def update_bfx_conn(
    conn_id: int,
    user: str,
    wallet: str,
    bfx_key: str,
    bfx_secret: str,
) -> int:
    await db.execute(
        """
        UPDATE bitfinex.connections SET
          user = ?
          wallet = ?,
          bfx_key = ?,
          bfx_secret = ?,
        WHERE id = ?
        """,
        (user, wallet, bfx_key, bfx_secret, conn_id),
    )
    return conn_id


async def get_bfx_conn(id: int) -> Optional[Connection]:
    row = await db.fetchone(
        "SELECT * FROM bitfinex.connections WHERE id = ?  LIMIT 1", (id,)
    )
    return Connection(**dict(row)) if row else None

async def get_or_create_conn(user: str) -> Optional[Connection]:
    row = await db.fetchone(
        "SELECT * FROM bitfinex.connections WHERE user = ?", (user,)
    )

    if not row:
        # create on the fly
        ls_id = await create_shop(wallet_id=wallet)
        return await get_shop(ls_id)

    return Shop(**dict(row)) if row else None

async def get_bfx_conns_by_user(user: str) -> List[Connection]:
    rows = await db.fetchall("SELECT * FROM bitfinex.connections WHERE user = ?", (user,))
    return [Connection(**dict(row)) for row in rows]


async def delete_bfx_conn(user: str, conn_id: int):
    await db.execute(
        """
        DELETE FROM bitfinex.connections WHERE user = ? AND id = ?
        """,
        (user, conn_id),
    )
