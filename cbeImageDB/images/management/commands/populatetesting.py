from django.core.management.base import BaseCommand
from . import management_methods as mm


class Command(BaseCommand):
    help = 'Populate the database with testing objects, no images or \
            experiments are created'

    def handle(self, *args, **options):
        mm.create_test_labs()
        print('Created testing labs')
        mm.create_test_experiment_objects()
        print('Created objects to make an experiment')
        mm.create_test_imager()
        print('Created an imager')
        mm.create_test_microscope_objects()
        print('Created microscope settings and associated objects')
        mm.create_test_organism()
        print('Created test organisms')
