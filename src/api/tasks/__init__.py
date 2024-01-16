from .celery import celery
from . import tasks  # noqa F401

__all__ = ["celery"]
