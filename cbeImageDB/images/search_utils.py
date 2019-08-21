from .models import MicroscopeSettings, Image, Experiment


def get_objectives():
    query = MicroscopeSettings.objects.all()
    objectives = []
    for ms in query:
        objectives.append(ms.objective)

    objectives = list(set(objectives))
    obj_string = []
    for o in objectives:
        if o.is_integer():
            obj_string.append(str(int(o)) + 'x')
        else:
            obj_string.append(str(o) + 'x')
    return obj_string


def month_string_to_int(month):
    months = ['January', 'Febuary', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November',
              'December']
    for i in range(0, 12):
        if month.lower() in months[i].lower():
            return (i + 1)


def get_year_list():
    years = []
    for i in Image.objects.all():
        years.append(i.date_taken.year)
    years = list(set(years))
    return years


def get_organism_list():
    organisms = []
    for i in Experiment.objects.all():
        for o in i.organism.all():
            organisms.append(o.organism_name)
    organisms = list(set(organisms))
    return organisms


def get_html_image_list(image, features=[]):
    # get the associated experiment
    e = image.experiment
    organism_list = ', '.join(str(o) for o in e.organism.all())
    lab_list = ', '.join([str(l) for l in e.lab.all()])
    # if there are no desired features, print them all
    if len(features) == 0:
        features = ['project', 'lab', 'imager', 'description', 'organism',
                    'microscope setting', 'vessel', 'growth substratum',
                    'file name', 'date taken', 'date uploaded']
    # Create a dictionary of possible lists
    f_dict = {'project': 'Project: {}'.format(e.project),
              'lab':
              'Lab(s): {}'.format(lab_list),
              'imager': 'Imager: {}'.format(image.imager),
              'date uploaded': 'Date Uploaded: {}'.format(image.date_uploaded),
              'date taken': 'Date Taken: {}'.format(image.date_taken),
              'organism': 'Organsim(s): {}'.format(organism_list),
              'microscope setting':
              'Microscope Setting: {}'.format(image.microscope_setting),
              'vessel': 'Vessel: {}'.format(e.vessel),
              'growth substratum':
              'Growth Substratum: {}'.format(e.substratum),
              'growth medium': 'Growth Medium: {}'.format(e.growth_medium),
              'file name':
              'File Name: {}'.format(image.document.name.split('/')[-1]),
              'search':
              '{}; {}'.format(organism_list, image.microscope_setting),
              'description': 'Description: {}'.format(image.brief_description),
              }

    # Hold the features wanted
    li = []
    for f in features:
        # get the feature from the dictonary
        try:
            li.append(f_dict[f])
        except KeyError:
            print('Key {} was not found in search_utils.{}'.format(f,
                  'get_html_image_list()'))

    return li


def get_html_experiment_list(experiment):
    organism_list = ', '.join(str(o) for o in experiment.organism.all())
    lab_list = ', '.join(str(l) for l in experiment.lab.all())
    li = ['Project: {}'.format(experiment.project),
          'Lab(s): {}'.format(lab_list),
          'Organism(s): {}'.format(organism_list),
          'Vessel: {}'.format(experiment.vessel),
          'Growth Substriatum: {}'.format(experiment.substratum),
          'Growth Medium: {}'.format(experiment.growth_medium)
          ]
    return li
