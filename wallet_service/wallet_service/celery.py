from __future__ import absolute_import, unicode_literals
import os
import environ
from celery import Celery
import logging


logger = logging.getLogger(__name__)

env = environ.Env()
environ.Env.read_env()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wallet_service.settings')

app = Celery('wallet_service')

logger.info(f"CELERY_BROKER_URL: {app.conf.broker_url}")

# Использование переменной окружения CELERY_BROKER_URL
app.conf.update(broker_url=env('CELERY_BROKER_URL'))

# Автоматический поиск задач
app.autodiscover_tasks()
