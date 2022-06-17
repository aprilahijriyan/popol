from typing import Dict

from popol.context.globals import state
from popol.context.proxy import LocalProxy

from .queue import Queue

saq_queue: Queue = LocalProxy(lambda: state.saq_queue)
saq_queues: Dict[str, Queue] = LocalProxy(lambda: state.saq_queues)
