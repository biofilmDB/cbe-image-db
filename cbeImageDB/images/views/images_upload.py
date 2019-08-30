from images import forms, models
from django.http import HttpResponseRedirect, HttpResponse  # , Redirect
import django.views.generic as genViews
from django.urls import reverse
from template_names import TemplateNames
from images import search_utils as su
from multi_form_view import MultiFormView
from django.template.loader import render_to_string


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
        # Render the results page
        success = {}
        success['user'] = self.request.user
        success['experiment'] = str(experiment)
        success['experiment_pk'] = experiment.id
        e = su.get_html_experiment_list(experiment)
        success['get_experiment_details'] = e
        feat = ['microscope setting', 'imager', 'date taken',
                'date uploaded']
        success['get_image_details'] = [su.get_html_image_dict(image, feat)]
        # import pdb; pdb.set_trace()
        rendered = render_to_string('images_upload/image_upload_success.html',
                                    success)
        return HttpResponse(rendered)


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
