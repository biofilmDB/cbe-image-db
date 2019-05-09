from django.shortcuts import render
from .forms import UploadFileForm
from django.http import HttpResponse  # Redirect
# from django.urls import reverse


# view to upload files, uses UploadFileForm
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_model = form.save(commit=False)

            # automatically get file name
            file_model.image_name = file_model.document.name

            # find temporary path to work with
            # temp_path = request.FILES['document'].temporary_file_path()

            # Save to model
            file_model.save()

            # easier when testing file upload
            return HttpResponse("Valid form. File committed.")
            # return HttpResponseRedirect(reverse('images:success',
            #                                     args=(file_model.id,)))
    else:
        form = UploadFileForm()
    return render(request, 'images/upload_file.html', {'form': form})
