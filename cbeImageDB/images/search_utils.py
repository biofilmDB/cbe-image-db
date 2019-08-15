from .models import Microscope_settings, Image


def get_objectives():
    query = Microscope_settings.objects.all()
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
    for i in Image.objects.all():
        for o in i.organism.all():
            organisms.append(o.organism_name)
    organisms = list(set(organisms))
    return organisms


def get_html_image_list(image):
    # get the associated experiment
    e = image.experiment
    organism_list = ', '.join(str(o) for o in e.organism.all())
    li = ['Project: {}'.format(e.project),
          'Lab(s): {}'.format(', '.join([str(l) for l in e.lab.all()])),
          'Imager: {}'.format(image.imager),
          'Date Uploaded: {}'.format(image.date_uploaded),
          'Organsim(s): {}'.format(organism_list),
          'Microscope Setting: {}'.format(image.microscope_setting),
          'Vessel: {}'.format(e.vessel),
          'Growth Substriatum: {}'.format(e.substratum),
          'Growth Medium: {}'.format(e.growth_medium),
          'File Name: {}'.format(image.document.name.split('/')[-1])
          ]
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
