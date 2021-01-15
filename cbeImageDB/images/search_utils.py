from .models import MicroscopeSettings, Image, Experiment
from datetime import datetime
from django.template.loader import render_to_string


def get_objectives():
    '''Gets all the possible objectives from the MicroscopeSettings
    and returns them as a list.'''
    # Get a list of all objectives used
    query = MicroscopeSettings.objects.all()
    objectives = []
    for ms in query:
        objectives.append(ms.objective)

    objectives = list(set(objectives))
    obj_string = []
    # Add an x to the end 63x
    for o in objectives:
        # Can be in both string or int format
        if o.is_integer():
            obj_string.append(str(int(o)) + 'x')
        else:
            obj_string.append(str(o) + 'x')
    return obj_string


def month_string_to_int(month):
    '''Converts month word to integer'''
    months = ['January', 'Febuary', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November',
              'December']
    for i in range(0, 12):
        if month.lower() in months[i].lower():
            return (i + 1)


def get_year_list():
    '''Returns only the years that images were taken in.'''
    years = []
    for i in Image.objects.all():
        years.append(i.date_taken.year)
    years = list(set(years))
    return years


def get_organism_list():
    '''Returns a list of organisms only used in images.'''
    organisms = []
    for i in Experiment.objects.all():
        for o in i.organism.all():
            organisms.append(o.name)
    organisms = list(set(organisms))
    return organisms


def get_html_image_list(image, features=[]):
    '''Returns a list of features about the image in the format (feature_name, 
    feature). If no features are passed in, all known features are returned.'''
    # get the associated experiment
    e = image.experiment
    organism_list = ', '.join(str(o) for o in e.organism.all())
    lab_list = ', '.join([str(l) for l in e.lab.all()])
    # if there are no desired features, print them all
    if len(features) == 0:
        features = ['experiment name', 'project', 'lab', 'imager',
                    'description', 'organism',
                    'microscope setting', 'vessel', 'growth substratum',
                    'file name', 'date taken', 'date uploaded', 'release date',
                    'raw data path']
    # Create a dictionary of possible lists
    f_dict = {'project': 'Project: {}'.format(e.project),
              'experiment name': 'Experiment Name: {}'.format(e.name),
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
              'file name':
              'File Name: {}'.format(image.document.name.split('/')[-1]),
              'search':
              '{}; {}'.format(organism_list, image.microscope_setting),
              'description': 'Description: {}'.format(image.brief_description),
              'release date':
              'Release Date: {}'.format(image.release_date),
              'raw data path':
              'Raw Data Path: {}'.format(image.path_to_raw_data),
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

    li_new = []
    # Split each list item on the :
    # So you can bold the descriptor (first element) in the html
    for f in li:
        f_list = f.split(': ')
        li_new.append([(f_list[0] + ': '), ': '.join(f_list[1:])])

    return li_new

    
def get_html_experiment_list(experiment):
    '''Returns list of features about the experiment in the format 
    (feature_name, feature).'''
    organism_list = ', '.join(str(o) for o in experiment.organism.all())
    lab_list = ', '.join(str(l) for l in experiment.lab.all())
    # Get list of all the asociated images
    images = experiment.image_set.all()
    dated = experiment.image_set.filter(release_date__lte=datetime.now())
    li = ['Name: {}'.format(experiment.name),
          'Project: {}'.format(experiment.project),
          'Lab(s): {}'.format(lab_list),
          'Organism(s): {}'.format(organism_list),
          'Vessel: {}'.format(experiment.vessel),
          'Growth Substriatum: {}'.format(experiment.substratum),
          'Total Images: {}'.format(len(images)),
          'Total Viewable Images: {}'.format(len(dated))
          ]

    # split them on the descriptor and description so the descriptor
    # can be bolded in html (name, some_experiment_name)
    li_new = []
    for f in li:
        f_list = f.split(': ')
        li_new.append([(f_list[0] + ': '), ': '.join(f_list[1:])])

    return li_new


def get_html_image_dict(image, features=[]):
    '''Returns a dictionary of image information that can be used on the 
    html pages to populate it with image information. It returns
    thumb, details, pk, release_date.'''
    # All images should have a large_thumb, but sometimes during testing
    # there were errors and they didn't
    try:
        url = image.large_thumb.url
    except ValueError:
        url = ''

    image_info_dict = {'thumb': url,
                       'details': get_html_image_list(image, features),
                       'pk': image.pk,
                       'release_date': image.release_date,
                       }
    return image_info_dict


def get_success_context(experiment, image):
    '''Returns a dictonary with experiment and image information to render
    a one-time success upload page.'''
    success = {}
    success['experiment'] = str(experiment)
    success['experiment_pk'] = experiment.id
    e = get_html_experiment_list(experiment)
    success['get_experiment_details'] = e
    # create list of select features for image details
    feat = ['microscope setting', 'imager', 'date taken',
            'date uploaded']
    success['get_image_details'] = [get_html_image_dict(image, feat)]
    return success


def image_details_to_html(image, thumb, fields=[]):
    context = {}
    context['thumb'] = thumb
    context['get_image_details'] = get_html_image_list(image, fields)
    rendered = render_to_string('images/image_details_template.html', context)
    return rendered
