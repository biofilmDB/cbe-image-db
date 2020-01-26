from django.core.management.base import BaseCommand
from . import management_methods as mm


class Command(BaseCommand):
    help = 'Setup the initial database'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--noorganisms',
            action='store_true',  # Don't knkow what action is
            help='Adds everything but the organisms',
        )

    def handle(self, *args, **options):
        # TODO: Create labs, growth medium, substratum
        print('\n#### Initializing Microscope Settings ####')
        mm.create_microscope_settings()
        print('\n#### Initializing Vessels ####')
        mm.create_vesssels()
        print('\n#### Initializing Growth Substratum ####')
        mm.create_substratum()
        print('\n#### Initializing Labs ####')
        mm.create_labs()

        if not options['noorganisms']:
            print('\n#### Initializing Organisms ####')
            print('This may take awhile')
            mm.create_organisms()
        else:
            print('\n#### Not Initializing Organisms ####')
            print('They can be created later by running populateorganisms')
