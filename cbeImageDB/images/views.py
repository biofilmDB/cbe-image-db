from . import forms
from django.http import HttpResponseRedirect  # , HttpResponse, Redirect
import django.views.generic as genViews
from .models import Image, Lab, Imager, Microscope_settings, Microscope, Medium
from django.urls import reverse
from dal import autocomplete
from django.utils.datastructures import MultiValueDictKeyError
from template_names import TemplateNames


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


class ImageThumbnailsView(TemplateNames, genViews.ListView):
    """ Shows all of the images that match a search criteria. At the moment,
    the only way to search is by lab."""
    model = Image
    context_object_name = 'image_list'
    paginate_by = 5

    def get_queryset(self):

        try:
            select_a_lab = self.request.GET['select_a_lab']
            return Image.objects.filter(lab__in=select_a_lab)
        except MultiValueDictKeyError:
            return []

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        try:
            select_a_lab = self.request.GET['select_a_lab']
            context['lab_name'] = Lab.objects.get(id=select_a_lab).pi_name
        except MultiValueDictKeyError:
            context['lab_name'] = 'Error in lab selection'
        return context


class SearchImageView(TemplateNames, genViews.FormView):
    """ Allows the users to search images by lab."""
    form_class = forms.SearchImageForm

    def get_success_url(self):
        return reverse('images:view_by_lab')


class UploadImageView(TemplateNames, genViews.CreateView):
    """ Allows the user to upload an image file and requests they fill in the
    model fields."""
    form_class = forms.UploadFileForm

    def form_valid(self, form):
        image = form.save()
        image.medium_thumb = image.document
        image.large_thumb = image.document
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
