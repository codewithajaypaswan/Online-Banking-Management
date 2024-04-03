from __future__ import absolute_import, unicode_literals
import os
import logging
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LoanManagementSystem.settings')

app = Celery('LoanManagementSystem')

app.config_from_object(settings, namespace='CELERY')

app.conf.broker_url = 'redis://localhost:6379/0'

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)
