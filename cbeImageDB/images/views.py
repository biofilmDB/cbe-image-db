from django.shortcuts import render
from .forms import UploadFileForm
from django.http import HttpResponseRedirect  # Redirect, HttpResponse
from django.views.generic import DetailView
from .models import Image
from django.urls import reverse
from django.conf import settings
import os


class ImageDetailsView(DetailView):
    model = Image
    template_name = 'images/image_upload_success.html'


# view to upload files, uses UploadFileForm
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)

            # automatically get file name
            image.image_name = image.document.name
            image.image_name = image.image_name.replace(' ', '_')
            image.document.name = image.image_name

            new_folder = str(image.lab).replace(' ', '_') + '/'
            lab_dir_path = settings.MEDIA_ROOT + '/' + new_folder
            # check if the lab path exists
            print(lab_dir_path)
            if not os.path.isdir(lab_dir_path):
                try:
                    os.mkdir(lab_dir_path)
                except OSError:
                    print('making directory failed')

            initial_path = image.document.path
            new_path = lab_dir_path + '/' + image.image_name
            os.rename(initial_path, new_path)

            # Save to model
            image.save()

            # easier when testing file upload
            # return HttpResponse("Valid form. File committed.")
            return HttpResponseRedirect(reverse('images:image_details',
                                                args=(image.id,)))
    else:
        form = UploadFileForm()
    return render(request, 'images/upload_file.html', {'form': form})
