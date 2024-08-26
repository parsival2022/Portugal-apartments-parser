from celery import shared_task
from django.contrib.sessions.models import Session
from django.utils import timezone
from .parser import ImovirtualParser

INIT_URL = 'https://www.imovirtual.com/en/comprar/apartamento/?locations%5B0%5D%5Bregion_id%5D=11&locations%5B0%5D%5Bsubregion_id%5D=163&locations%5B1%5D%5Bregion_id%5D=11&locations%5B1%5D%5Bsubregion_id%5D=162'

@shared_task
def cleanup_expired_sessions():
    expired_sessions = Session.objects.filter(expire_date__lt=timezone.now())
    expired_sessions.delete()

@shared_task
def task_launch_parser():
    try:
       parser = ImovirtualParser(INIT_URL)
       parser.data_extraction()
    except Exception as e:
        print(e)
