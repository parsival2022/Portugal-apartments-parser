from django.core.management.base import BaseCommand
from api.managers import AdsManager as am

class Command(BaseCommand):
    help = 'creates history from database'

    def handle(self, *args, **options):
        am.create_and_save_history()
        print('history created')