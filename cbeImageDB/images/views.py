from django.shortcuts import render, redirect
from .forms import UploadFileForm, SearchImageForm
from django.http import HttpResponseRedirect, HttpResponse  # Redirect
from django.views.generic import DetailView, ListView, FormView
from .models import Image, Lab
from django.urls import reverse


class ImageDetailsView(DetailView):
    model = Image
    template_name = 'images/image_upload_success.html'

"""
def ImageThumbnails(request, pk):
    image_list = Image.objects.filter(lab=pk)
    lab_list = Lab.objects.filter(id=pk)
    if len(lab_list) > 0:
        lab_list = 'Images: {}'.format(lab_list[0].name)
    else:
        lab_list = 'Lab id {} does not exist'.format(pk)
    context = {'image_list': image_list, 'lab_list': lab_list}
    return render(request, 'images/view_images.html', context)
"""


class ImageThumbnailsView(ListView):
    model = Image
    context_object_name = 'image_list'
    template_name = 'images/view_images.html'
    # paginate_by = 20

    def get_queryset(self):
        import pdb; pdb.set_trace()
        # lab = self.request.GET.get('selected_labs', 'default')
        lab = self.kwargs['selected_labs']
        print(lab)
        return Image.objects.filter(lab=1)



class SearchImageView(FormView):
    template_name = 'images/search_images.html'
    form_class = SearchImageForm
    success_url = 'images/view_images.html'

    def form_valid(self, form):
        selected_labs = form.cleaned_data.get('selected_labs')
        return_string = 'Labs selected were: ' + str(selected_labs)
        import pdb; pdb.set_trace()
        return HttpResponseRedirect('images/view_by_lab/')

    def get(self, request):
        import pdb; pdb.set_trace()
        lab = self.request.GET['selected_labs']
        return redirect('view_by_lab/', selected_labs=lab)

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
