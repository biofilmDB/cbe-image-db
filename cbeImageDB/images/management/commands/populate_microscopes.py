from django.core.management.base import BaseCommand
from images.models import Objective, Microscope


class Command(BaseCommand):

    def _create_objectives(self):
        # Make sure the ordering is correct
        Objective.objects.all().delete()
        # add new objectives
        Objective(objective='2.5X', medium='air').save()
        Objective(objective='5X', medium='air').save()
        Objective(objective='10X', medium='air').save()
        Objective(objective='40X', medium='air').save()
        Objective(objective='63X', medium='air').save()
        Objective(objective='1.25X', medium='air').save()
        Objective(objective='20X', medium='water').save()
        Objective(objective='63X', medium='water').save()
        Objective(objective='63X', medium='oil').save()
        Objective(objective='63X', medium='glycerin').save()

    def _create_microscopes(self):
        # create list of objectives in above order
        obj = Objective.objects.all()

        # delete all microscopes so existing objectives don't get messed up
        Microscope.objects.all().delete()
        Microscope(microscope_name='Laser Microdisection Scope',
                   objective=obj[0]).save()
        Microscope(microscope_name='Laser Microdisection Scope',
                   objective=obj[1]).save()
        Microscope(microscope_name='Laser Microdisection Scope',
                   objective=obj[2]).save()
        Microscope(microscope_name='Laser Microdisection Scope',
                   objective=obj[3]).save()
        Microscope(microscope_name='Laser Microdisection Scope',
                   objective=obj[4]).save()
        Microscope(microscope_name='Inverted Confocal Microscope ',
                   objective=obj[5]).save()
        Microscope(microscope_name='Inverted Confocal Microscope ',
                   objective=obj[2]).save()
        Microscope(microscope_name='Inverted Confocal Microscope ',
                   objective=obj[6]).save()
        Microscope(microscope_name='Inverted Confocal Microscope ',
                   objective=obj[7]).save()
        Microscope(microscope_name='Inverted Confocal Microscope ',
                   objective=obj[8]).save()
        Microscope(microscope_name='Inverted Confocal Microscope ',
                   objective=obj[9]).save()

    def handle(self, *args, **options):
        self._create_objectives()
        self._create_microscopes()
