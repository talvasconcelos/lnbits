from quart import Blueprint
from lnbits.db import Database

db = Database("ext_copilot")


copilot_ext: Blueprint = Blueprint(
    "copilot", __name__, static_folder="static", template_folder="templates"
)


from .views_api import *  # noqa
from .views import *  # noqa