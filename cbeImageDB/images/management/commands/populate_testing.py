from django.core.management.base import BaseCommand
from images import models as m


class Command(BaseCommand):
    help = 'Creates two labs, test lab 1 and 2 and an imager Jane Doe'

    def _create_labs(self):
        tl1 = m.Lab(pi_name='test lab 1')
        tl1.save()

        tl2 = m.Lab(pi_name='test lab 2')
        tl2.save()

    def _create_imager(self):
        m.Imager(imager_name='Jane Doe').save()

    def _create_microscope(self):
        med = m.Medium(medium_type="Plasma")
        med.save()
        mic = m.Microscope(microscope_name='Test Scope')
        mic.save()
        m.Microscope_settings(microscope=mic, objective=63, medium=med).save()

    def _create_organism(self):
        m.Organism.objects.create(organism_name='Test organism', storid='123',
                                  ncbi_id='ncbi25')

    def _create_experiment_objects(self):
        m.Vessel.objects.create(name='Test Reactor A')
        m.GrowthSubstratum.objects.create(substratum='Test Glass')
        m.GrowthMedium.objects.create(growth_medium='Test growth medium')

    def handle(self, *args, **options):
        self._create_labs()
        self._create_imager()
        self._create_microscope()
        self._create_organism()
        self._create_experiment_objects()
