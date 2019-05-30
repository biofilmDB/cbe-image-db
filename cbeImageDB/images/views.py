from django.shortcuts import render
from .forms import UploadFileForm
from django.http import HttpResponseRedirect  # Redirect, HttpResponse
from django.views.generic import DetailView, ListView
from .models import Image, Lab
from django.urls import reverse


class ImageDetailsView(DetailView):
    model = Image
    template_name = 'images/image_upload_success.html'


class ImageThumbnailsView(ListView):
    model = Image
    context_object_name = 'image_list'
    template_name = 'images/view_images.html'
    paginate_by = 20

    def get_querylist():
        return Image.objects.all()


# view to upload files, uses UploadFileForm
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)

            # automatically get file name
            image.image_name = image.document.name
            # image.image_name = image.image_name.replace(' ', '_')
            image.document.name = image.image_name
            image.path = image.document.path

            # Save to model
            image.save()
            # easier when testing file upload
            # return HttpResponse("Valid form. File committed.")
            return HttpResponseRedirect(reverse('images:image_details',
                                                args=(image.id,)))
    else:
        form = UploadFileForm()
    return render(request, 'images/upload_file.html', {'form': form})
