from . import forms
from django.http import HttpResponseRedirect  # , HttpResponse, Redirect
import django.views.generic as genViews
from .models import Image, Lab, Imager, Microscope_settings, Microscope, Medium, Organism
from django.urls import reverse
from dal import autocomplete
from django.utils.datastructures import MultiValueDictKeyError
from template_names import TemplateNames
from . import search_utils as su
from django import http
from datetime import datetime
from .documents import ImageDocument
from multi_form_view import MultiFormView


class AddImagerView(genViews.CreateView):
    """ Allows a user to ad an imager using a webpage. It uses a genaric create
    model template."""
    template_name = 'images/create_model.html'
    form_class = forms.AddImagerForm
    model = Imager

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading1'] = "Add a new Imager"
        context['intro_p'] = "Type your name into the box to add yourself as "
        context['intro_p'] += "an imager."
        context['button_text'] = "Add"
        return context


class ImagerSuccessView(TemplateNames, genViews.DetailView):
    model = Imager


class UploadImageView(TemplateNames, MultiFormView):
    """ Allows the user to upload an image file and requests they fill in the
    model fields."""
    form_classes = {
        'image_form': forms.UploadFileForm,
        'experiment_form': forms.CreateExperimentForm,
    }
    def forms_valid(self, forms):
        experiment = forms['experiment_form'].save()
        experiment.save()
        image = forms['image_form'].save(commit=False)
        image.experiment = experiment
        image.medium_thumb.save(name=image.document.name,
                                content=image.document)
        image.large_thumb.save(name=image.document.name,
                               content=image.document)
        image.save()
        return HttpResponseRedirect(reverse('images:image_details',
                                            args=(image.id,)))


class ImageDetailsView(TemplateNames, genViews.DetailView):
    """ Shows the details of an image. It is where a sucessfull image upload is
    redirected to."""
    model = Image


# Search all searchable terms at the same time
class GeneralSearchView(genViews.FormView):
    form_class = forms.GeneralSearchImageForm
    template_name = 'images/search_images.html'


def get_description_search_qs(request, qs):

    try:
        desct = request.GET.get('description_search')
        if desct != '':
            s = ImageDocument.search().query("match", brief_description=desct)
            qs = qs & s.to_queryset()

    except MultiValueDictKeyError:
        pass
    return qs


class GeneralSearchResultsView(genViews.ListView):
    model = Image
    context_object_name = 'image_list'
    template_name = 'images/image_search_results.html'
    paginate_by = 5

    def get_queryset(self):
        if self.request.user.is_superuser:
            qs = Image.objects.all()
        else:
            qs = Image.objects.filter(release_date__lte=datetime.now())

        try:
            search_list = self.request.GET.getlist('search')
            for search in search_list:
                q = search.split(': ')
                if q[0].lower() == 'imager':
                    qs = qs.filter(imager__imager_name=q[-1])

                # elif q[0].lower() == 'lab':
                #    qs = qs.filter(lab__pi_name=q[-1])

                elif q[0].lower() == 'objective medium':
                    qs = qs.filter(microscope_setting__medium__medium_type=q[-1])

                elif q[0].lower() == 'objective':
                    # remove x from objective
                    obj = float(q[-1][:-1])
                    qs = qs.filter(microscope_setting__objective=obj)

                elif q[0].lower() == 'microscope':
                    qs = qs.filter(microscope_setting__microscope__microscope_name=q[-1])
                # elif q[0].lower() == 'organism':
                #    qs = qs.filter(organism__organism_name=q[-1])
                elif q[0].lower() == 'day':
                    qs = qs.filter(date_taken__day=q[-1])
                elif q[0].lower() == 'month':
                    month = su.month_string_to_int(q[-1])
                    qs = qs.filter(date_taken__month=month)
                elif q[0].lower() == 'year':
                    qs = qs.filter(date_taken__year=q[-1])

        except MultiValueDictKeyError:
            pass

        qs = get_description_search_qs(self.request, qs)

        return qs


# Search by attributes
class AttributeSearchImageView(TemplateNames, genViews.FormView):
    """ Allows the users to search images by selecting criteria for attributes
    of the image"""
    form_class = forms.AttributeSearchImageForm


class AttributeSearchResultsView(genViews.ListView):
    """ Shows all of the images that match a search criteria."""
    model = Image
    context_object_name = 'image_list'
    template_name = 'images/image_search_results.html'
    paginate_by = 5

    def get_queryset(self):
        if self.request.user.is_superuser:
            qs = Image.objects.all()
        else:
            qs = Image.objects.filter(release_date__lte=datetime.now())

        # Variable to tell if there was something that was searched
        """
        try:
            search_lab = self.request.GET['lab']
            if search_lab != '':
                qs = qs.filter(lab=search_lab)
        except MultiValueDictKeyError:
            pass
        """

        try:
            search_imager = self.request.GET['imager']
            if search_imager != '':
                qs = qs.filter(imager=search_imager)
        except MultiValueDictKeyError:
            pass

        try:
            search_objective = self.request.GET['objective']
            if search_objective != '':
                qs = qs.filter(microscope_setting__objective=search_objective)

        except MultiValueDictKeyError:
            pass

        try:
            microscope = self.request.GET['microscope']
            if microscope != '':
                qs = qs.filter(microscope_setting__microscope=microscope)
        except MultiValueDictKeyError:
            pass

        try:
            obj_medium = self.request.GET['objective_medium']
            if obj_medium != '':
                qs = qs.filter(microscope_setting__medium=obj_medium)
        except MultiValueDictKeyError:
            pass

        try:
            day = self.request.GET['day_taken']
            if day != '':
                qs = qs.filter(date_taken__day=day)
        except MultiValueDictKeyError:
            pass

        try:
            month = self.request.GET['month_taken']
            if month != '':
                month = su.month_string_to_int(month)
                qs = qs.filter(date_taken__month=month)
        except MultiValueDictKeyError:
            pass

        try:
            year = self.request.GET['year_taken']
            if year != '':
                qs = qs.filter(date_taken__year=year)
        except MultiValueDictKeyError:
            pass

        """
        try:
            organ = self.request.GET['organism']
            if organ != '':
                qs = qs.filter(organism=organ)
        except MultiValueDictKeyError:
            pass
        """

        qs = get_description_search_qs(self.request, qs)

        return qs


# ######################### Autocomplete classes #############################
class MicroscopeSettingAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        settings = Microscope_settings.objects.all()
        scopes = Microscope.objects.all()
        mediums = Medium.objects.all()

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
        qs = Microscope.objects.all()

        if self.q:
            qs = qs.filter(microscope_name__icontains=self.q)

        return qs


class MediumAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Medium.objects.all()
        if self.q:
            qs = qs.filter(medium_type__icontains=self.q)
        return qs


class ImagerAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Imager.objects.all()
        if self.q:
            qs = qs.filter(imager_name__icontains=self.q)
        return qs


class OrganismAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Organism.objects.all()
        if self.q:
            qs = qs.filter(organism_name__icontains=self.q)
        return qs


class AddImagerAutocomplete(autocomplete.Select2QuerySetView):

    # Overwrite method from autocomplete
    # Only give the option of creating a new imager if the value does not exist
    # somewhere in the imager names
    def get_create_option(self, context, q):
        display_create_option = False
        create_object = []

        possibles = Imager.objects.filter(imager_name__icontains=q)
        if len(possibles) == 0:
            display_create_option = True
            create_object = [{'id': q,
                              'text': 'Add imager: {}'.format(q),
                             'create_id': True}]
        return create_object

    # post method is only called when creating a new object
    def post(self, request):
        text = request.POST.get('text', None)
        if text is None:
            return http.HttpResponseBadRequest()
        result = Imager.objects.create(imager_name=text)
        return http.JsonResponse({
            'id': result.pk,
            'text': self.get_result_label(result),
        })

    def get_queryset(self):
        qs = Imager.objects.all()
        if self.q:
            qs = qs.filter(imager_name__icontains=self.q)
        return qs


class LabAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Lab.objects.all()
        if self.q:
            qs = qs.filter(pi_name__icontains=self.q)
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


class SearchAutocomplete(autocomplete.Select2ListView):

    def get_list(self):
        search_terms = []
        # ['Lab: ' + str(x) for x in list(Lab.objects.all())]
        search_terms.extend(['Imager: ' + str(x) for x in
                            list(Imager.objects.all())])
        search_terms.extend(['Microscope: ' + str(x) for x in
                            list(Microscope.objects.all())])
        search_terms.extend(['Objective Medium: ' + str(x) for x in
                             list(Medium.objects.all())])
        search_terms.extend(['Objective: ' + x for x in su.get_objectives()])
        #search_terms.extend(['Organism: ' + x for x in su.get_organism_list()])
        search_terms.extend(['Day: ' + str(x) for x in range(1, 32)])
        months = ['January', 'Febuary', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November',
                  'December']
        search_terms.extend(['Month: ' + x for x in months])
        search_terms.extend(['Year: ' + str(x) for x in su.get_year_list()])
        return search_terms
