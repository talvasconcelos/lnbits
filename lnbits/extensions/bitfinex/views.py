from quart import g, render_template

from lnbits.decorators import check_user_exists, validate_uuids

from . import bitfinex_ext


@bitfinex_ext.route("/")
@validate_uuids(["usr"], required=True)
@check_user_exists()
async def index():
    return await render_template("bitfinex/index.html", user=g.user)
