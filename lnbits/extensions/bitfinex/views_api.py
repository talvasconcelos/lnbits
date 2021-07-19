# views_api.py is for you API endpoints that could be hit by another service

from quart import g, jsonify
from http import HTTPStatus
from lnbits.decorators import api_check_wallet_key, api_validate_post_request
from crud import (
    add_bfx_conn,
    get_bfx_conn,
    update_bfx_conn,
    get_bfx_conns_by_user
)

from . import bitfinex_ext


# add your endpoints here


@bitfinex_ext.route("/api/v1/bitfinex", methods=["POST"])
@bitfinex_ext.route("/api/v1/bitfinex/<conn_id>", methods=["PUT"])
@api_check_wallet_key("admin")
@api_validate_post_request(
    schema={
        "user": {"type": "string", "empty": False, "required": True},
        "wallet": {"type": "string", "empty": False, "required": True},
        "bfx_key": {"type": "string", "empty": False, "required": True},
        "bfx_secret": {"type": "string", "empty": False, "required": True},
    }
)
async def api_add_or_update_conn(conn_id=None):
    shop = await get_or_create_conn(g.wallet.id)
# async def api_bitfinex():
#     """Try to add descriptions for others."""
#     tools = [
#         {
#             "name": "Quart",
#             "url": "https://pgjones.gitlab.io/quart/",
#             "language": "Python",
#         },
#         {
#             "name": "Vue.js",
#             "url": "https://vuejs.org/",
#             "language": "JavaScript",
#         },
#         {
#             "name": "Quasar Framework",
#             "url": "https://quasar.dev/",
#             "language": "JavaScript",
#         },
#     ]
#
#     return jsonify(tools), HTTPStatus.OK
