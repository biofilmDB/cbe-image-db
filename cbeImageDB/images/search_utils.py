from .models import Microscope_settings, Image, Microscope


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


def search_microscope_name(name, init_image_qs):
    mic = Microscope.objects.all()
    mic = mic.filter(microscope_name=name)
    ms = Microscope_settings.objects.none()
    # use a for loop in case multiple microscopes get returned
    for m in mic:
        ms = ms | Microscope_settings.objects.filter(microscope=m)

    # find images for the settings
    new_qs = Image.objects.none()
    for m in ms:
        new_qs = new_qs | init_image_qs.filter(microscope_setting=m)

    return new_qs
