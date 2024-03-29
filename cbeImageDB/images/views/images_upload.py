from images import forms, models
from django.http import HttpResponse  # , Redirect
import django.views.generic as genViews
from django.views.generic.edit import FormView
from template_names import TemplateNames
from images import search_utils as su
from multi_form_view import MultiFormView
from django.template.loader import render_to_string
from django.db import transaction
from decouple import config
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse


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


class PickExperimentView(TemplateNames, genViews.TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get all experiments to use in the html for the names and attributes
        context['names'] = models.Experiment.objects.order_by('name')
        # get queryset of experiments ordered by name
        exps = models.Experiment.objects.order_by('name')
        exps_dict = {}  # make dictionary to store all experiments in
        # got through each exp, get info and add to dictionary
        # i will be how the javascript will index each experiment
        for i,e in enumerate(exps):
            edict = {}
            elist = su.get_html_experiment_list(e)
            # convert list into dictonary
            for l in elist:
               edict[l[0]] = l[1]
            # add the redirect path for the url as the last entry in the
            # dictionary
            edict['View Experiment Details Page'] = reverse('images:experiment_details',
                                                    args=(e.pk,))
            # ints must be strings for js to be happy
            exps_dict[str(i)] = edict
        # turn to string and replace ' with " for proper json formatting
        context['experiments'] = str(exps_dict).replace("'", '"')
        return context

    def post(self, request, *args, **kwargs):
        pk = request.POST['names']
        return HttpResponseRedirect(reverse('images:upload_image_to_experiment',
                                            args=(int(pk),)))


class UploadImageView(TemplateNames, MultiFormView):
    """ Allows the user to upload an image file and requests they fill in the
    model fields."""
    form_classes = {
        'image_form': forms.UploadFileForm,
        'experiment_form': forms.CreateExperimentForm,
    }

    def forms_valid(self, forms):
        files = self.request.FILES.getlist('image')
        images = []
        try:
            with transaction.atomic():
                experiment = forms['experiment_form'].save()
                experiment.save()
                image = forms['image_form']
                images = image.make_image_models(experiment.pk, files)
        except Exception as e:
            print(e)
            # TODO: Redirect to an error page of some kind
            # pop up error box and redirect to upload page?
            return HttpResponse('ERROR {}'.format(e))
        pks = []
        for image in images:
            pks.append(image.pk)
        return HttpResponseRedirect(reverse('images:update_uploaded_images',
                                            args=(pks,)))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # make a dictionary of experiment names so they can be read into
        # javascript
        exp = list(models.Experiment.objects.all().order_by('name'))
        context['experiment_names'] = str({'names': [e.name for e in exp]}).replace("'", '"')

        context['support_name'] = config('SUPPORT_NAME')
        context['support_email'] = config('SUPPORT_EMAIL')

        return context


class UploadImageToExperimentView(TemplateNames, genViews.DetailView,
                                  FormView):
    model = models.Experiment
    form_class = forms.UploadFileForm
    # success_url = reverse_lazy('images:upload')

    def form_valid(self, form):
        files = self.request.FILES.getlist('image')
        images = []
        try:
            images = form.make_image_models(self.kwargs['pk'], files)
        except Exception as e:
            print(e)
            # TODO: Redirect to an error page of some kind
            # pop up error box and redirect to upload page?
            return HttpResponse('<h1>NOTHING uploaded error: {}</h1>'.format(e))

        experiment = models.Experiment.objects.get(id=self.kwargs['pk'])
        pks = []
        for image in images:
            pks.append(image.pk)
        return HttpResponseRedirect(reverse('images:update_uploaded_images',
                                            args=(pks,)))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the image
        e = kwargs['object']
        context['get_experiment_details'] = su.get_html_experiment_list(e)
        return context
