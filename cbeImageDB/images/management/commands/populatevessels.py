from django.core.management.base import BaseCommand
from . import management_methods as mm


class Command(BaseCommand):
    help = 'Create all the known possible vessels to use (reactors)'

    def handle(self, *args, **options):
        mm.create_vesssels()
