from django.shortcuts import render
from .forms import UploadFileForm, SearchImageForm
from django.http import HttpResponseRedirect  # , HttpResponse, Redirect
from django.views.generic import DetailView, ListView, FormView
from .models import Image, Lab
from django.urls import reverse


class ImageDetailsView(DetailView):
    model = Image
    template_name = 'images/image_upload_success.html'


class ImageThumbnailsView(ListView):
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
        context['lab_name'] = Lab.objects.get(id=select_a_lab).name
        return context


class SearchImageView(FormView):
    template_name = 'images/search_images.html'
    form_class = SearchImageForm
    success_url = 'images/view_images.html'


# view to upload files, uses UploadFileForm
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.save()
            return HttpResponseRedirect(reverse('images:image_details',
                                                args=(image.id,)))
    else:
        form = UploadFileForm()
    return render(request, 'images/upload_file.html', {'form': form})
