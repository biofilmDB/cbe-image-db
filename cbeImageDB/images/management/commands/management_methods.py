import pandas
from images.models import Organism, Microscope, Medium, Microscope_settings
from images.models import Imager, Lab, Project, Vessel, GrowthMedium
from images.models import GrowthSubstratum


def create_vesssels():
    vessel_list = ['CDC', 'Drip Flow', 'Capillary', 'Membrane Filter',
                   'Annular', 'Rotating Disk']
    for vessel in vessel_list:
        print('Added vessel: {}'.format(vessel))
        Vessel.objects.create(name=vessel)


def create_organisms():
    csv = pandas.read_csv('organisms/organisms.csv', sep='|')

    print('Total number of organisms to add: {}'.format(len(csv)))
    for index, row in csv.iterrows():
        if index % 5000 == 0 and index != 0:
            print('Added organism number: {}'.format(index))

        Organism.objects.create(storid=row[0], ncbi_id=row[1],
                                organism_name=row[2])


def create_microscope_medium():
    mediums = ['air', 'water', 'oil', 'glycerin', 'dry']
    medium_list = []
    for med in mediums:
        m = Medium(medium_type=med)
        m.save()
        medium_list.append(m)
    return medium_list


def create_microscopes():
    scopes = ['Laser Microdisection Scope', 'Inverted Confocal Microscope',
              'Upright Confocal Microscope', 'Leica Steroscope',
              'Epifluorescent Microscope', 'Nikon Steroscope', 'Bio-Raman']
    microscope_list = []
    for scope in scopes:
        m = Microscope(microscope_name=scope)
        m.save()
        microscope_list.append(m)
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
        ms = Microscope_settings(microscope=microscope_list[combo[0]],
                                 objective=float(combo[1]),
                                 medium=medium_list[combo[2]])
        ms.save()
        print('Added: {}'.format(ms))


def create_test_labs():
    tl1 = Lab(pi_name='test lab 1')
    tl1.save()

    tl2 = Lab(pi_name='test lab 2')
    tl2.save()


def create_test_imager():
    Imager(imager_name='Jane Doe').save()


def create_test_microscope_objects():
    med = Medium(medium_type="Plasma (Test)")
    med.save()
    mic = Microscope(microscope_name='Test Scope')
    mic.save()
    Microscope_settings(microscope=mic, objective=63, medium=med).save()


def create_test_organism():
    Organism.objects.create(organism_name='Fluffy Stuff (Test organism)',
                            storid='123', ncbi_id='ncbi25')
    Organism.objects.create(organism_name='Squishy Goo (Test organism)',
                            storid='567', ncbi_id='ncbi66')


def create_test_experiment_objects():
    Project.objects.create(name='Test Exploration of Mystical Bacteria')
    Vessel.objects.create(name='Test Reactor A')
    GrowthSubstratum.objects.create(substratum='Dimond (Test)')
    GrowthMedium.objects.create(growth_medium='Fruit Juice (Test)')
