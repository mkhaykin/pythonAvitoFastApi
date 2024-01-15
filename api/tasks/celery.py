import logging

from celery import Celery  # type: ignore

from api.config import settings

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND

logger = logging.getLogger(__name__)
