from django.core.management.base import BaseCommand
from .import management_commands as mm


class Command(BaseCommand):
    help = "Reads in a list of organisms from a file named organisms.csv and \
            populates the database"

    def handle(self, *args, **options):
        mm.create_organisms()
