from django.core.management.base import BaseCommand
from . import management_methods as mm


class Command(BaseCommand):
    help = 'Creates a known list of the microscopes avaliable for imaging'

    def handle(self, *args, **options):
        mm.create_microscope_settings()
