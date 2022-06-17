from typing import Any, Dict

from fastapi import FastAPI

from ...utils import get_settings
from .config import parse_config
from .queue import Queue


def setup(app: FastAPI, settings: Any = None) -> Dict[str, Queue]:
    """
    Install the saq plugin to the app.
    This will install 2 new attributes to `app.state` which are:

    * `saq_queue` - SAQ Queue (Default, if available)
    * `saq_queues` - All SAQ queues (dict type)

    Args:
        app: FastAPI app.
        settings: The settings (can be pydantic.BaseSettings).

    Returns:
        Dict[str, Queue]: The SAQ queues.
    """

    settings = get_settings(app, settings)
    queue_maps, _ = parse_config(settings)
    app.state.saq_queue = queue_maps.get("default")
    app.state.saq_queues = queue_maps
    return queue_maps
