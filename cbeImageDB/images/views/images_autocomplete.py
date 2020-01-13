'''All of the autocomplete views are stored here accept for the search
autocomplete view, because it is more involved. Some autocompletes have
the capability to add new models others do not.'''
from images import models
from dal import autocomplete
from images import search_utils as su


# ######################### Autocomplete classes #############################
# SearchAutocopmlete is in images_search.py
class MicroscopeSettingAutocomplete(autocomplete.Select2QuerySetView):
    '''Will bring up the microscope setting when searching with associated
    scopes, mediums, and objectives.'''
    def get_queryset(self):
        # List of all things possible to filter by
        settings = models.MicroscopeSettings.objects.all()
        scopes = models.Microscope.objects.all()
        mediums = models.ObjectiveMedium.objects.all()

        if self.q:
            # filter by objective
            qs = settings.filter(objective__istartswith=self.q)

            # Filter by scope
            scopes_filter = scopes.filter(name__icontains=self.q)
            for mic in scopes_filter:
                qs = qs | settings.filter(microscope=mic)

            # filter by medium
            mediums_filter = mediums.filter(name__istartswith=self.q)
            for med in mediums_filter:
                qs = qs | settings.filter(medium=med)

        else:
            qs = settings
        return qs


class MicroscopeAutocomplete(autocomplete.Select2QuerySetView):
    '''Autocomplete: return a list of all the microscopes'''

    def get_queryset(self):
        qs = models.Microscope.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class ObjectiveMediumAutocomplete(autocomplete.Select2QuerySetView):
    '''Autocomplete: Returns a list of all the microscope objective mediums'''
    def get_queryset(self):
        qs = models.ObjectiveMedium.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class OrganismAutocomplete(autocomplete.Select2QuerySetView):
    '''Autocomplete: Return a list of all organisms'''
    def get_queryset(self):
        qs = models.Organism.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class ImagerAutocomplete(autocomplete.Select2QuerySetView):
    '''Autocomplete: Return a list of all imagers'''
    def get_queryset(self):
        qs = models.Imager.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class AddImagerAutocomplete(autocomplete.Select2QuerySetView):
    '''Autocomplete: Can add an imager if not in the list of all imagers'''
    create_field = 'name'
    model = models.Imager
    model_field_name = 'name'


    def has_add_permission(self, request):
        return True


class ProjectAutocomplete(autocomplete.Select2QuerySetView):
    '''Autocomplete: Return a list of all projects'''
    def get_queryset(self):
        qs = models.Project.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class AddProjectAutocomplete(autocomplete.Select2QuerySetView):
    '''Autocomplete: Add a project if doesn't exist in the list of all 
    projects returned'''
    create_field = 'name'
    model = models.Project
    model_field_name = 'name'


    def has_add_permission(self, request):
        return True


class LabAutocomplete(autocomplete.Select2QuerySetView):
    '''Autocomplete: Return a list of all labs'''
    def get_queryset(self):
        qs = models.Lab.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class GrowthSubstratumAutocomplete(autocomplete.Select2QuerySetView):
    '''Autocomplete: Return a list of all growth substratum'''
    def get_queryset(self):
        qs = models.GrowthSubstratum.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class VesselAutocomplete(autocomplete.Select2QuerySetView):
    '''Autocomplete: Return list of vessels sample was grown in'''
    def get_queryset(self):
        qs = models.Vessel.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class DayAutocomplete(autocomplete.Select2ListView):
    '''Autocomplete: Returns the numbers 1-31 for days of the month'''
    def get_list(self):
        return range(1, 32)


class MonthAutocomplete(autocomplete.Select2ListView):
    '''Autocomplete: Returns list of all possible months'''
    def get_list(self):
        months = ['January', 'Febuary', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November',
                  'December']
        return months


class YearAutocomplete(autocomplete.Select2ListView):
    '''Autocomplete: Returns a list of years that exist in the database'''
    def get_list(self):
        return su.get_year_list()
