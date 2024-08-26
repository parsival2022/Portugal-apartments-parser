import os
from celery import Celery





os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parser.settings')

app = Celery('parser')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()



# app.conf.beat_schedule = {
#     'launch_parser': {
#         'task': 'api.tasks.task_launch_parser',
#         'schedule': 30.0
#     },
#     'clear_sessions': {
#         'task': 'api.tasks.cleanup_expired_sessions',
#         'schedule': 30.0
#     }
# }

app.conf.timezone = 'UTC'

