from popol.context.globals import state
from popol.context.proxy import LocalProxy

from . import Database

db: Database = LocalProxy(lambda: state.db)
