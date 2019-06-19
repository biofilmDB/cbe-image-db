from . import forms
from django.http import HttpResponseRedirect  # , HttpResponse, Redirect
import django.views.generic as genViews
from .models import Image, Lab, Imager
from django.urls import reverse
from dal import autocomplete
from django.utils.datastructures import MultiValueDictKeyError


class ImagerAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Imager.objects.all()
        if self.q:
            qs = qs.filter(imager_name__istartswith=self.q)
        return qs


class LabAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Lab.objects.all()
        if self.q:
            qs = qs.filter(pi_name__istartswith=self.q)
        return qs


class AddImagerView(genViews.CreateView):
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


class ImageDetailsView(genViews.DetailView):
    model = Image
    template_name = 'images/image_upload_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab_list = kwargs['object'].lab.all()
        # import ipdb; ipdb.set_trace()
        lab_list_str = ''
        if len(lab_list) > 0:
            lab_list = [str(x) for x in lab_list]
            lab_list_str = ', '.join(lab_list)
        context['image_lab'] = lab_list_str

        context['image_name'] = kwargs['object'].document.name
        context['image_name'] = context['image_name'].split('/')[-1]


        return context

class ImageThumbnailsView(genViews.ListView):
    model = Image
    context_object_name = 'image_list'
    template_name = 'images/view_images.html'
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


class SearchImageView(genViews.FormView):
    template_name = 'images/search_images.html'
    form_class = forms.SearchImageForm
    success_url = 'images/view_images.html'


class UploadImageView(genViews.CreateView):
    form_class = forms.UploadFileForm
    template_name = 'images/upload_file.html'


    def form_valid(self, form):
        # import ipdb; ipdb.set_trace()
        image = form.save()
        image.save()
        # import ipdb; ipdb.set_trace()
        return HttpResponseRedirect(reverse('images:image_details',
                                            args=(image.id,)))
