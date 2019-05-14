from django.shortcuts import render
from .forms import UploadFileForm
from django.http import HttpResponse  # Redirect
# from django.urls import reverse


# view to upload files, uses UploadFileForm
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)

            # automatically get file name
            image.image_name = str(image.lab) + '_' + image.document.name
            image.path = image.document.path

            # find temporary path to work with
            # temp_path = request.FILES['document'].temporary_file_path()

            # Save to model
            image.save()

            # easier when testing file upload
            return HttpResponse("Valid form. File committed.")
            # return HttpResponseRedirect(reverse('images:success',
            #                                     args=(file_model.id,)))
    else:
        form = UploadFileForm()
    return render(request, 'images/upload_file.html', {'form': form})
