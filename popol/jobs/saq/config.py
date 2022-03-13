from typing import Any, Dict, Tuple

from .queue import Queue


def parse_config(settings: Any) -> Tuple[Dict[str, Queue], Dict[str, dict]]:
    """
    SAQ configuration parsing.

    Args:
        settings: The settings (can be pydantic.BaseSettings).

    Returns:
        Tuple[Dict[str, Queue], Dict[str, dict]]: The SAQ queues and the queue settings.
    """

    saq_queues: Dict[str, dict] = getattr(settings, "SAQ_QUEUES", {})
    if not isinstance(saq_queues, dict):
        raise RuntimeError("SAQ_QUEUES must be a dict, got {}".format(type(saq_queues)))

    queue_maps = {}
    queue_settings = {}
    for q_name, q_param in saq_queues.items():
        url = q_param.get("url", None)
        if not url:
            raise RuntimeError("No url specified for queue {}".format(q_name))

        queue = Queue.from_url(url, q_name)
        queue_maps[q_name] = queue
        queue_settings[q_name] = q_param
    return queue_maps, queue_settings
