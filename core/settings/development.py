from core.settings.base import *

# Celery Settings
CELERY_WORKER_POOL = 'solo'

CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

CELERY_TASK_SERIALZIER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'Asia/Kabul'
CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_ENABLE_UTC = True
