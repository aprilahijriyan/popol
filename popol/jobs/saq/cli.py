import asyncio

from saq.worker import Worker
from typer import Option, Typer, echo

from ...utils import get_settings, load_app
from .config import parse_config

saq = Typer(name="saq", help="SAQ Worker")


@saq.command()
def runworker(queue: str = Option(..., help="Queue to run (e.g. default)")):
    """
    Run the SAQ worker.
    """

    app = load_app()
    settings = get_settings(app)
    queue_maps, queue_settings = parse_config(settings)
    if queue not in queue_maps:
        raise RuntimeError("Queue {0!r} not found in settings".format(queue))

    q_setting = queue_settings[queue]
    queue_obj = queue_maps[queue]
    functions = q_setting.pop("functions", [])
    startup = q_setting.pop("startup", None)
    if startup and not asyncio.iscoroutinefunction(startup):
        raise RuntimeError("startup must be a coroutine")

    default_ctx = q_setting.pop("context", {})
    if not isinstance(default_ctx, dict):
        raise RuntimeError("context must be a dict")

    async def x_startup(ctx: dict):
        ctx.update(default_ctx)
        ctx["app"] = app
        ctx["state"] = app.state
        if startup:
            await startup(ctx)

    q_setting.pop("url", None)
    q_setting["startup"] = x_startup
    worker = Worker(queue_obj, functions, **q_setting)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    echo("Starting SAQ worker... (Press CTRL-C to exit)")
    try:
        loop.run_until_complete(worker.start())
    finally:
        loop.stop()


@saq.command()
def list_queue():
    """
    List queues.
    """

    app = load_app()
    settings = get_settings(app)
    queue_maps, queue_settings = parse_config(settings)
    for q_name, queue in queue_maps.items():
        echo(f"* {q_name} ({queue.url}): {queue_settings[q_name]}")
