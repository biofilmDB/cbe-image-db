from django.core.management.base import BaseCommand
from . import management_methods as mm


class Command(BaseCommand):
    help = 'Creates a known list of the growth substratum'

    def handle(self, *args, **options):
        mm.create_substratum()
