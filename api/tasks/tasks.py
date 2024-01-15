import asyncio
from typing import Any

from .celery import Celery, celery, logger


async def my_async_task(**kwargs: Any) -> None:  # noqa U100
    logger.info("hello")


@celery.task()
def my_task(**kwargs: Any) -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(my_async_task(**kwargs))


@celery.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs: Any) -> None:  # noqa U100
    print(type(sender))
    sender.add_periodic_task(
        schedule=10,
        sig=my_task.s(),
        name="my task",
    )
