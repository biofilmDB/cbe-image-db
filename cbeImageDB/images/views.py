from django.shortcuts import render
from . import forms
from django.http import HttpResponseRedirect  # , HttpResponse, Redirect
import django.views.generic as genViews
from .models import Image, Lab, Imager
from django.urls import reverse
from dal import autocomplete


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


class ImageThumbnailsView(genViews.ListView):
    model = Image
    context_object_name = 'image_list'
    template_name = 'images/view_images.html'
    paginate_by = 5

    def get_queryset(self):
        # import ipdb; ipdb.set_trace()
        select_a_lab = self.request.GET['select_a_lab']
        self.kwargs['select_a_lab'] = select_a_lab
        # import ipdb; ipdb.set_trace()
        return Image.objects.filter(lab=select_a_lab)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # TODO: Figure out what to put for defualt, becuase it gives an error
        select_a_lab = self.request.GET.get('select_a_lab', 'default')
        context['lab_name'] = Lab.objects.get(id=select_a_lab).pi_name
        return context


class SearchImageView(genViews.FormView):
    template_name = 'images/search_images.html'
    form_class = forms.SearchImageForm
    success_url = 'images/view_images.html'


# view to upload files, uses UploadFileForm
def upload_file(request):
    if request.method == 'POST':
        form = forms.UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.save()
            return HttpResponseRedirect(reverse('images:image_details',
                                                args=(image.id,)))
    else:
        form = forms.UploadFileForm()
    return render(request, 'images/upload_file.html', {'form': form})
