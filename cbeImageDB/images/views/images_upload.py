from images import forms, models
from django.http import HttpResponseRedirect  # , HttpResponse, Redirect
import django.views.generic as genViews
from django.urls import reverse
from template_names import TemplateNames
from images import search_utils as su
from multi_form_view import MultiFormView


class UploadImageView(TemplateNames, MultiFormView):
    """ Allows the user to upload an image file and requests they fill in the
    model fields."""
    form_classes = {
        'image_form': forms.UploadFileForm,
        'experiment_form': forms.CreateExperimentForm,
    }

    def forms_valid(self, forms):
        experiment = forms['experiment_form'].save()
        experiment.save()
        image = forms['image_form'].save(commit=False)
        image.experiment = experiment
        image.medium_thumb.save(name=image.document.name,
                                content=image.document)
        image.large_thumb.save(name=image.document.name,
                               content=image.document)
        image.save()
        return HttpResponseRedirect(reverse('images:upload_success',
                                            args=(experiment.id,)))


class ImageUploadSuccessView(TemplateNames, genViews.DetailView):
    """ Shows the details of an image. It is where a sucessfull image upload is
    redirected to."""
    model = models.Experiment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the image
        e = kwargs['object']
        images = e.image_set.order_by('-pk')
        context['get_experiment_details'] = su.get_html_experiment_list(e)
        context['get_image_details'] = []
        # Make dictionarys for each image
        for image in images:
            t = su.get_html_image_dict(image, ['microscope setting', 'imager',
                                               'date taken', 'date uploaded'])
            context['get_image_details'].append(t)
        return context


class UploadImageToExperimentView(TemplateNames, genViews.DetailView,
                                  genViews.CreateView):
    model = models.Experiment
    form_class = forms.UploadFileForm
    # success_url = reverse_lazy('images:upload')

    def form_valid(self, form):
        image = form.save(commit=False)
        image.experiment = models.Experiment.objects.get(id=self.kwargs['pk'])
        image.medium_thumb.save(name=image.document.name,
                                content=image.document)
        image.large_thumb.save(name=image.document.name,
                               content=image.document)
        image.save()
        return HttpResponseRedirect(reverse('images:upload_success',
                                            args=(image.experiment.id,)))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the image
        e = kwargs['object']
        # TODO: Not sure what this is doing. Is it needed?
        # images = e.image_set.all()
        context['get_experiment_details'] = su.get_html_experiment_list(e)
        return context
