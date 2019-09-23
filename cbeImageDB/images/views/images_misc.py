from images import forms, models
import django.views.generic as genViews
from template_names import TemplateNames
from images import search_utils as su
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from datetime import datetime, date
from django.core.exceptions import PermissionDenied


class AboutSite(TemplateNames, genViews.TemplateView):
    pass


class ExperimentDetailsView(TemplateNames, genViews.ListView):
    model = models.Image
    context_object_name = 'image_obj_list'
    paginate_by = 15

    def get_queryset(self):
        e = models.Experiment.objects.get(id=self.kwargs['experiment'])
        qs = e.image_set.all()

        if not self.request.user.is_superuser:
            qs = qs.filter(release_date__lte=datetime.now())

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        e = models.Experiment.objects.get(id=self.kwargs['experiment'])
        context['experiment'] = str(e)
        context['experiment_pk'] = e.pk
        context['get_experiment_details'] = su.get_html_experiment_list(e)
        context['get_image_details'] = []
        # Make dictionarys for each image
        for image in context['image_obj_list']:
            t = su.get_html_image_dict(image, ['microscope setting', 'imager',
                                               'date taken', 'date uploaded',
                                               'release date'])
            context['get_image_details'].append(t)

        return context


class ImageDetailsView(TemplateNames, genViews.DetailView):
    """ Shows the details of an image. It is where a sucessfull image upload is
    redirected to."""
    model = models.Image

    def get_object(self):
        try:
            img = models.Image.objects.get(pk=self.kwargs['pk'])
        except models.Image.DoesNotExist:
            error = "Image with id: {} does not exist.".format(
                self.kwargs['pk'])
            raise Http404(error)
        rd = img.release_date
        if rd > date.today() and not self.request.user.is_superuser:
                error = "You do not have permission to view this image due to \
                         its release date."
                raise PermissionDenied(error)
        else:
            return img

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the image
        image = kwargs['object']
        context['get_image_details'] = su.get_html_image_list(image)
        return context


class UpdateImageView(TemplateNames, genViews.UpdateView):
    model = models.Image
    form_class = forms.UploadFileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        image = models.Image.objects.get(id=self.kwargs['pk'])
        e = image.experiment
        context['experiment_data'] = su.get_html_experiment_list(e)
        return context

    def form_valid(self, form):
        image = form.save(commit=False)

        image.medium_thumb.save(name=image.document.name,
                                content=image.document)
        image.large_thumb.save(name=image.document.name,
                               content=image.document)
        image.save()
        return HttpResponseRedirect(reverse('images:image_details',
                                            args=(image.id,)))
