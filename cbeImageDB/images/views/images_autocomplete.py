from images import models
from dal import autocomplete
from images import search_utils as su
from django import http


# ######################### Autocomplete classes #############################
# SearchAutocopmlete is in search.py
class MicroscopeSettingAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        settings = models.MicroscopeSettings.objects.all()
        scopes = models.Microscope.objects.all()
        mediums = models.ObjectiveMedium.objects.all()

        if self.q:
            # filter by objective
            qs = settings.filter(objective__istartswith=self.q)

            # Filter by scope
            scopes_filter = scopes.filter(microscope_name__icontains=self.q)
            for mic in scopes_filter:
                qs = qs | settings.filter(microscope=mic)

            # filter by medium
            mediums_filter = mediums.filter(medium_type__istartswith=self.q)
            for med in mediums_filter:
                qs = qs | settings.filter(medium=med)

        else:
            qs = settings
        return qs


class MicroscopeAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = models.Microscope.objects.all()

        if self.q:
            qs = qs.filter(microscope_name__icontains=self.q)

        return qs


class ObjectiveMediumAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = models.ObjectiveMedium.objects.all()
        if self.q:
            qs = qs.filter(medium_type__icontains=self.q)
        return qs


class ImagerAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = models.Imager.objects.all()
        if self.q:
            qs = qs.filter(imager_name__icontains=self.q)
        return qs


class OrganismAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = models.Organism.objects.all()
        if self.q:
            qs = qs.filter(organism_name__icontains=self.q)
        return qs


class AddImagerAutocomplete(autocomplete.Select2QuerySetView):
    create_field = 'imager_name'

    def get_queryset(self):
        qs = models.Imager.objects.all()
        if self.q:
            qs = qs.filter(imager_name__icontains=self.q)
        return qs


class LabAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = models.Lab.objects.all()
        if self.q:
            qs = qs.filter(pi_name__icontains=self.q)
        return qs


class GrowthMediumAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = models.GrowthMedium.objects.all()
        if self.q:
            qs = qs.filter(growth_medium__icontains=self.q)
        return qs


class GrowthSubstratumAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = models.GrowthSubstratum.objects.all()
        if self.q:
            qs = qs.filter(substratum__icontains=self.q)
        return qs


class VesselAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = models.Vessel.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class ProjectAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = models.Project.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class DayAutocomplete(autocomplete.Select2ListView):

    def get_list(self):
        return range(1, 32)


class MonthAutocomplete(autocomplete.Select2ListView):

    def get_list(self):
        months = ['January', 'Febuary', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November',
                  'December']
        return months


class YearAutocomplete(autocomplete.Select2ListView):

    def get_list(self):
        return su.get_year_list()
