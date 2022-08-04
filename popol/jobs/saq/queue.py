from typing import Callable

try:
    from redis.asyncio.client import Redis
    from saq.job import Job
    from saq.queue import Queue as _Queue

except ImportError:
    errMsg = "SAQ is not installed. Please install it with `pip install saq`"
    raise RuntimeError(errMsg)

from popol import json


def _json_dumps(*args, **kwargs):
    data = json.dumps(*args, **kwargs)
    if isinstance(data, bytes):
        data = data.decode("utf-8")
    return data


class Queue(_Queue):
    @classmethod
    def from_url(
        cls,
        url: str,
        name: str = "popol",
        dump: Callable = _json_dumps,
        load: Callable = json.loads,
        **kwargs,
    ) -> "Queue":
        """Create SAQ queue"""
        return cls(url, name=name, dump=dump, load=load, **kwargs)

    def __init__(
        self,
        url: str,
        *,
        name: str = "popol",
        dump: Callable = json.dumps,
        load: Callable = json.loads,
        **kwargs,
    ):
        """
        Initialize a queue.

        Args:
            url: The redis url.
            name: The queue name.
            dump: Function to serialize job to redis.
            load: Function to deserialize job from redis.
        """

        self.url = url
        redis = Redis.from_url(url, **kwargs)
        super().__init__(redis, name, dump, load)

    async def enqueue(self, job_or_func, **kwargs) -> Job:
        """
        Enqueue a job.
        """
        return await super().enqueue(job_or_func, **kwargs)
