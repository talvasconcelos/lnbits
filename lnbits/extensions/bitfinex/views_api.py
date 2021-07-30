# views_api.py is for you API endpoints that could be hit by another service

from quart import g, jsonify
from http import HTTPStatus
from lnbits.decorators import api_check_wallet_key, api_validate_post_request
from .crud import (
    add_bfx_conn,
    get_bfx_conn,
    update_bfx_conn,
    get_bfx_conns_by_user
)

from . import bitfinex_ext


# add your endpoints here

@bitfinex_ext.route("/api/v1/bitfinex", methods=["GET"])
@api_check_wallet_key("invoice")
async def api_conns_from_user():
    conns = await get_bfx_conns_by_user(g.wallet.user)
    try:
        return (
            jsonify([{**conn._asdict()} for conn in conns]),
            HTTPStatus.OK,
        )
    except:
        return "", HTTPStatus.NO_CONTENT

@bitfinex_ext.route("/api/v1/bitfinex/connection", methods=["POST"])
@bitfinex_ext.route("/api/v1/bitfinex/connection/<conn_id>", methods=["PUT"])
@api_check_wallet_key("admin")
@api_validate_post_request(
    schema={
        "user": {"type": "string", "empty": False, "required": True},
        "name": {"type": "string", "empty": False, "required": True},
        "wallet": {"type": "string", "empty": False, "required": True},
        "key": {"type": "string", "empty": False, "required": True},
        "secret": {"type": "string", "empty": False, "required": True},
    }
)
async def api_add_or_update_conn(conn_id=None):
    if conn_id == None:
        await add_bfx_conn(
            g.data["name"],
            g.data["user"],
            g.data["wallet"],
            g.data["key"],
            g.data["secret"]
        )
        return "", HTTPStatus.CREATED
    else:
        await update_bfx_conn(
            g.data["conn_id"],
            g.data["name"],
            g.data["key"],
            g.data["secret"]
        )
        return "", HTTPStatus.OK
    
