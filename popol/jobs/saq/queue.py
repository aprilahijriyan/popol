from typing import Callable

try:
    from aioredis.client import Redis
    from saq.job import Job
    from saq.queue import Queue as _Queue

except ImportError:
    errMsg = "SAQ is not installed. Please install it with `pip install saq`"
    raise RuntimeError(errMsg)

from popol.json import json


class Queue(_Queue):
    @classmethod
    def from_url(
        cls,
        url: str,
        name: str = "popol",
        dump: Callable = json.dumps,
        load: Callable = json.loads,
        **kwargs,
    ) -> "Queue":
        """Create a queue with a redis url a name."""
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
