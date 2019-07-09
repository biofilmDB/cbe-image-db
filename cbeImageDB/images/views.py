from . import forms
from django.http import HttpResponseRedirect  # , HttpResponse, Redirect
import django.views.generic as genViews
from .models import Image, Lab, Imager, Microscope_settings, Microscope, Medium
from django.urls import reverse
from dal import autocomplete
from django.utils.datastructures import MultiValueDictKeyError
from template_names import TemplateNames
from . import search_utils as su


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

    def form_valid(self, form):
        new_imager = form.save()
        new_imager.save()
        return HttpResponseRedirect(reverse('images:upload'))


class ImageDetailsView(TemplateNames, genViews.DetailView):
    """ Shows the details of an image. It is where a sucessfull image upload is
    redirected to."""
    model = Image

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab_list = kwargs['object'].lab.all()
        # import ipdb; ipdb.set_trace()
        lab_list_str = ''
        if len(lab_list) > 0:
            lab_list = [str(x) for x in lab_list]
            lab_list_str = ', '.join(lab_list)
        context['image_lab'] = lab_list_str

        return context


# Search all searchable terms at the same time
class GeneralSearchView(genViews.FormView):
    form_class = forms.GeneralSearchImageForm
    template_name = 'images/search_images.html'


class GeneralSearchResultsView(genViews.ListView):
    model = Image
    context_object_name = 'image_list'
    template_name = 'images/image_search_results.html'
    paginate_by = 5

    def get_queryset(self):
        qs = Image.objects.all()
        try:
            search_list = self.request.GET.getlist('search')
            for search in search_list:
                q = search.split(': ')
                if q[0].lower() == 'imager':
                    qs = qs.filter(imager__imager_name=q[-1])

                elif q[0].lower() == 'lab':
                    qs = qs.filter(lab__pi_name=q[-1])

                elif q[0].lower() == 'medium':
                    qs = qs.filter(microscope_setting__medium__medium_type=q[-1])

                elif q[0].lower() == 'objective':
                    # remove x from objective
                    obj = float(q[-1][:-1])
                    qs = qs.filter(microscope_setting__objective=obj)

                elif q[0].lower() == 'microscope':
                    qs = qs.filter(microscope_setting__microscope__microscope_name=q[-1])

        except MultiValueDictKeyError:
            pass
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
        qs = Image.objects.all()
        try:
            search_lab = self.request.GET['search_lab']
            if search_lab != '':
                qs = qs.filter(lab__in=search_lab)
        except MultiValueDictKeyError:
            pass

        try:
            search_imager = self.request.GET['search_imager']
            if search_imager != '':
                qs = qs.filter(imager__in=search_imager)
        except MultiValueDictKeyError:
            pass

        try:
            search_objective = self.request.GET['search_objective']
            if search_objective != '':
                ms = Microscope_settings.objects.all()
                ms = ms.filter(objective=search_objective)
                new_qs = Image.objects.none()
                for m in ms:
                    new_qs = new_qs | qs.filter(microscope_setting=m)
                qs = new_qs
        except MultiValueDictKeyError:
            pass

        return qs


class UploadImageView(TemplateNames, genViews.CreateView):
    """ Allows the user to upload an image file and requests they fill in the
    model fields."""
    form_class = forms.UploadFileForm

    def form_valid(self, form):
        image = form.save()
        image.save()
        return HttpResponseRedirect(reverse('images:image_details',
                                            args=(image.id,)))


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


class ImagerAutocomplete(autocomplete.Select2QuerySetView):

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


class SearchAutocomplete(autocomplete.Select2ListView):

    def get_list(self):
        # TODO: Get list of all possible search keys and find a way to link
        # them back to the objects they came from
        search_terms = ['Lab: ' + str(x) for x in list(Lab.objects.all())]
        search_terms.extend(['Imager: ' + str(x) for x in
                            list(Imager.objects.all())])
        search_terms.extend(['Microscope: ' + str(x) for x in
                            list(Microscope.objects.all())])
        search_terms.extend(['Medium: ' + str(x) for x in
                             list(Medium.objects.all())])
        search_terms.extend(['Objective: ' + x for x in su.get_objectives()])
        return search_terms
