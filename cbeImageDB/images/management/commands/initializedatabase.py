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
        print('\n#### Initializing Microscope Settings ####')
        ms = mm.create_microscope_settings()
        print('\n#### Initializing Vessels ####')
        v = mm.create_vesssels()
        print('\n#### Initializing Growth Substratum ####')
        s = mm.create_substratum()
        print('\n#### Initializing Labs ####')
        l = mm.create_labs()

        if not options['noorganisms']:
            print('\n#### Initializing Organisms ####')
            print('This may take awhile')
            o = mm.create_organisms()
            if not o:
                print('No organisms file. Please run organisms/parse_ncbi.py ',
                      'to create the organisms list')
        else:
            print('\n#### Not Initializing Organisms ####')
            print('They can be created later by running populateorganisms')
        if not v:
            print('Vessels not created, please add vessels.txt file to create ',
                  'vessels')
        if not s:
            print('Substratum not created, please add a substratum.txt file ',
                  'to create substratum.')
        if not l:
            print('Labs not created, please add a labs.txt file to create labs')

