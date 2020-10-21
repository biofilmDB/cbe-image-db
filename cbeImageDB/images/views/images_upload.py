from images import forms, models
from django.http import HttpResponse  # , Redirect
import django.views.generic as genViews
from template_names import TemplateNames
from images import search_utils as su
from multi_form_view import MultiFormView
from django.template.loader import render_to_string
from django.db import transaction
from decouple import config


# Render image so users can't return to the page if the release
# date is in the future. It just generates a one time string to return
def render_upload_success(obj, image, experiment):
    success = su.get_success_context(experiment, image)
    success['image_pk'] = image.pk
    success['experiment_name'] = experiment.name
    success['user'] = obj.request.user
    rendered = render_to_string('images_upload/image_upload_success.html',
                                success)
    return rendered


class UploadImageView(TemplateNames, MultiFormView):
    """ Allows the user to upload an image file and requests they fill in the
    model fields."""
    form_classes = {
        'image_form': forms.UploadFileForm,
        'experiment_form': forms.CreateExperimentForm,
    }

    def forms_valid(self, forms):
        with transaction.atomic():
            experiment = forms['experiment_form'].save()
            experiment.save()
            image = forms['image_form'].save(commit=False)
            image.experiment = experiment
            image.medium_thumb.save(name=image.document.name,
                                    content=image.document)
            image.large_thumb.save(name=image.document.name,
                                   content=image.document)
            image.save()
            # Render the results page
            rendered = render_upload_success(self, image, experiment)
        return HttpResponse(rendered)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['support_name'] = config('SUPPORT_NAME')
        context['support_email'] = config('SUPPORT_EMAIL')
        
        # NOTE: This is entered because the experiment name is a pain
        exp = list(models.Experiment.objects.all().order_by('name'))
        context['experiment_names'] = ', '.join([e.name for e in exp])

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

        # Render the results page
        experiment = models.Experiment.objects.get(id=self.kwargs['pk'])
        rendered = render_upload_success(self, image, experiment)
        return HttpResponse(rendered)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the image
        e = kwargs['object']
        # TODO: Not sure what this is doing. Is it needed?
        # images = e.image_set.all()
        context['get_experiment_details'] = su.get_html_experiment_list(e)
        return context
