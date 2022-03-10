from typing import Any, Dict

from fastapi import FastAPI

from ...utils import get_settings
from .config import parse_config
from .queue import Queue


def setup(app: FastAPI, settings: Any = None) -> Dict[str, Queue]:
    settings = get_settings(app, settings)
    queue_maps, _ = parse_config(settings)
    app.state.queue = queue_maps.get("default")
    app.state.queues = queue_maps
    return queue_maps
