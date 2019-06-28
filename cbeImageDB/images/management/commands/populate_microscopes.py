from django.core.management.base import BaseCommand
from images.models import Medium, Microscope, Microscope_settings


class Command(BaseCommand):
    # hold values to keep in order
    medium_list = []
    microscope_list = []

    def _create_medium(self):
        mediums = ['air', 'water', 'oil', 'glycerin']
        for med in mediums:
            m = Medium(medium_type=med)
            m.save()
            self.medium_list.append(m)

    def _create_microscopes(self):
        scopes = ['Laser Microdisection Scope', 'Inverted Confocal Microscope',
                  'Upright Confocal Microscope', 'Leica Steroscope',
                  'Epifluorescent Microscope', 'Nikon Steroscope', 'Bio-Raman']
        for scope in scopes:
            m = Microscope(microscope_name=scope)
            m.save()
            self.microscope_list.append(m)

    def _create_microscope_settings(self):
        # make alist of combos (microscope, objective, medium)
        # Assume same order as previously listed
        combos = [(0, 2.5, 0), (0, 5, 0), (0, 10, 0), (0, 20, 0), (0, 63, 0),
                  (1, 1.25, 0), (1, 10, 0), (1, 20, 1), (1, 63, 1), (1, 63, 2),
                  (1, 63, 3)]
        for combo in combos:
            ms = Microscope_settings(microscope=self.microscope_list[combo[0]],
                                     objective=float(combo[1]),
                                     medium=self.medium_list[combo[2]])
            ms.save()
            print('Added: {}'.format(ms))

    def handle(self, *args, **options):
        self._create_medium()
        self._create_microscopes()
        self._create_microscope_settings()
