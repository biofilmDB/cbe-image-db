from django.core.management.base import BaseCommand
from images.models import Lab, Imager, Microscope, Microscope_settings, Medium


class Command(BaseCommand):
    help = 'Creates two labs, test lab 1 and 2 and an imager Jane Doe'

    def _create_labs(self):
        tl1 = Lab(pi_name='test lab 1')
        tl1.save()

        tl2 = Lab(pi_name='test lab 2')
        tl2.save()

    def _create_imager(self):
        Imager(imager_name='Jane Doe').save()

    def _create_microscope(self):
        med = Medium(medium_type="Plasma")
        med.save()
        mic = Microscope(microscope_name='Test Scope')
        mic.save()
        Microscope_settings(microscope=mic, objective=63, medium=med).save()

    def handle(self, *args, **options):
        self._create_labs()
        self._create_imager()
        self._create_microscope()
