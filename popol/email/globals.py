from popol.context.globals import state
from popol.context.proxy import LocalProxy

from .backend import EmailBackend

email: EmailBackend = LocalProxy(lambda: state.email)
