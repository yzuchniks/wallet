from __future__ import absolute_import, unicode_literals

import logging
import os

from celery import Celery

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wallet_service.settings')

app = Celery('wallet_service')

logger.info(f"CELERY_BROKER_URL: {app.conf.broker_url}")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
