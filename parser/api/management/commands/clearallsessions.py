from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session

class Command(BaseCommand):
    help = 'Deletes all the sessions'

    def handle(self, *args, **options):
        sessions = Session.objects.all()
        sessions.delete()