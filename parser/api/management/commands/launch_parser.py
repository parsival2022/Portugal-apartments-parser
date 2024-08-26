from django.core.management.base import BaseCommand
from api.parser import ImovirtualParser, IMOVIRTUAL_URL

class Command(BaseCommand):
    help = 'Launch the parser'

    def handle(self, *args, **options):
        try:
          parser = ImovirtualParser(IMOVIRTUAL_URL)
          parser.data_extraction()
        except Exception as e:
          print(e)


