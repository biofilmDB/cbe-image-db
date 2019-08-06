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
        organisms.append(i.organism.organism_name)
    organisms = list(set(organisms))
    return organisms
