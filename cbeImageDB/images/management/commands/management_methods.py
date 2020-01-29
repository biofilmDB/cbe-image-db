import pandas
from images.models import Microscope, ObjectiveMedium, MicroscopeSettings
from images.models import Imager, Lab, Project, Vessel
from images.models import GrowthSubstratum, Organism


def create_substratum():
    GrowthSubstratum.objects.get_or_create(name='other')
    print('Created GrowthSubstratum: other')
    try:
        with open('substratum2.txt') as f:
            for line in f:
                GrowthSubstratum.objects.get_or_create(name=line.strip())
                print('Created GrowthSubstratum: {}'.format(line.strip()))
    except FileNotFoundError:
        print('Not loading substratum. Please create a file substratum.txt')
        return False
    return True


def create_vesssels():
    Vessel.objects.get_or_create(name="other")
    print('Created Vessel: other')
    try:
        with open('vessels2.txt') as f:
            for line in f:
                Vessel.objects.get_or_create(name=line.strip())
                print('Created Vessel: {}'.format(line.strip()))
    except FileNotFoundError:
        return False
    return True

def create_labs():
    try:
        with open('labs2.txt') as f:
            for line in f:
                Lab.objects.get_or_create(name=line.strip())
                print('Created Lab: {}'.format(line.strip()))
    except FileNotFoundError:
        return False
    return True

def create_organisms():
    try:
        csv = pandas.read_csv('organisms/organisms2.csv', sep='|')

        print('Total number of organisms to add: {}'.format(len(csv)))
        for index, row in csv.iterrows():
            if index % 5000 == 0 and index != 0:
                print('Added organism number: {}'.format(index))

            Organism.objects.get_or_create(storid=row[0], ncbi_id=row[1],
                                           name=row[2])
    except FileNotFoundError:
        return False
    return True

def create_microscope_medium():
    mediums = ['air', 'water', 'oil', 'glycerin', 'dry']
    medium_list = []
    for med in mediums:
        m = ObjectiveMedium.objects.get_or_create(name=med)
        medium_list.append(m[0])
    return medium_list


def create_microscopes():
    scopes = ['Laser Microdisection Scope', 'Inverted Confocal Microscope',
              'Upright Confocal Microscope', 'Leica Steroscope',
              'Epifluorescent Microscope', 'Nikon Steroscope', 'Bio-Raman']
    microscope_list = []
    for scope in scopes:
        m = Microscope.objects.get_or_create(name=scope)
        microscope_list.append(m[0])
    return microscope_list


def create_microscope_settings():
    microscope_list = create_microscopes()
    medium_list = create_microscope_medium()
    # make alist of combos (microscope, objective, medium)
    # Assume same order as previously listed
    combos = [(0, 2.5, 0), (0, 5, 0), (0, 10, 0), (0, 40, 0), (0, 63, 0),
              (1, 1.25, 0), (1, 10, 0), (1, 20, 1), (1, 63, 1), (1, 63, 2),
              (1, 63, 3), (2, 1.25, 0), (2, 10, 0), (2, 10, 1), (2, 20, 0),
              (2, 25, 1), (2, 40, 1), (2, 63, 1), (3, 1, 0), (3, 2, 0),
              (4, 1, 0), (4, 4, 0), (4, 10, 0), (4, 20, 0), (4, 20, 1),
              (4, 40, 1), (4, 40, 2), (4, 50, 4), (4, 60, 1), (4, 100, 2),
              (5, 1, 0), (6, 10, 0), (6, 50, 0), (6, 60, 1), (6, 100, 0)]

    for combo in combos:
        ms = MicroscopeSettings.objects.get_or_create(microscope=microscope_list[combo[0]],
                                                      objective=float(combo[1]),
                                                      medium=medium_list[combo[2]])
        print('Added: {}'.format(ms[0]))


def create_test_labs():
    Lab.objects.get_or_create(name='test lab 1')
    Lab.objects.get_or_create(name='test lab 2')


def create_test_imager():
    Imager.objects.get_or_create(name='Jane Doe')


def create_test_microscope_objects():
    med = ObjectiveMedium.objects.get_or_create(name="Plasma (Test)")
    mic = Microscope.objects.get_or_create(name='Test Scope')
    MicroscopeSettings.objects.get_or_create(microscope=mic[0], objective=63,
                                             medium=med[0])


def create_test_organism():
    Organism.objects.get_or_create(name='Fluffy Stuff (Test organism)',
                                   storid='123', ncbi_id='ncbi25')
    Organism.objects.get_or_create(name='Squishy Goo (Test organism)',
                                   storid='567', ncbi_id='ncbi66')


def create_test_experiment_objects():
    Project.objects.get_or_create(name='Test Exploration of Mystical Bacteria')
    Vessel.objects.get_or_create(name='Test Reactor A')
    GrowthSubstratum.objects.get_or_create(name='Dimond (Test)')
