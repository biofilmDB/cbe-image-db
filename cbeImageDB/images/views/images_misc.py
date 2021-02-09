from images import forms, models, help_texts as ht
import django.views.generic as genViews
from template_names import TemplateNames
from images import search_utils as su
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from datetime import datetime, date
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db import transaction, IntegrityError
from django.template.loader import render_to_string


class AboutSite(TemplateNames, genViews.TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help_text_experiment'] = ht.experiment_name
        context['help_text_project'] = ht.experiment_project
        return context

###############################################################################
# DETAIL VIEWS # DETAIL VIEWS # DETAIL VIEWS # DETAIL VIEWS # DETAIL VIEWS # DET
###############################################################################
class ExperimentDetailsView(TemplateNames, genViews.ListView):
    model = models.Image
    context_object_name = 'image_obj_list'
    paginate_by = 15

    def get_queryset(self):
        e = get_object_or_404(models.Experiment, pk=self.kwargs['experiment'])
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
            error = "Image with id {} does not exist.".format(
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


###############################################################################
# UPDATE VIEWS # UPDATE VIEWS # UPDATE VIEWS # UPDATE VIEWS # UPDATE VIEWS # UPD
###############################################################################
class UpdateExperimentView(TemplateNames, genViews.UpdateView):
    model = models.Experiment
    form_class = forms.CreateExperimentForm

    def get_object(self):
        try:
            # get the current experiment
            exp = models.Experiment.objects.get(pk=self.kwargs['pk'])
        # raise 404 error if it is not found
        except models.Experiment.DoesNotExist:
            error = "Experiment with id {} does not exist.".format(
                self.kwargs['pk'])
            raise Http404(error)

        # riase 403 error if experiment is not editable and user is not a
        # superuser
        if not exp.is_editable and not self.request.user.is_superuser:
            dc = exp.date_created
            pk = exp.pk
            url = reverse('images:experiment_details', args=(pk,))
            html = "<h2> Experiment Not Editable </h2> \
                <p>The allowed time to update this experiment has passed. \
                The creation date for this experiment is {}. \
                If you need to edit this image, please contact an admin and \
                have them edit the experiment with id {}. \
                Click <a href=\"{}\">here</a> to view the experiment details. \
                </p>".format(dc, pk, url)

            raise PermissionDenied(html)
        else:
            return exp

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the experiment and all images associated with it
        # NOTE: Not worrying about the release date here, because this page
        # should only be viewable within 24 hours of an experiment creation for
        # general users
        e = get_object_or_404(models.Experiment, pk=self.kwargs['pk'])
        images = e.image_set.all()

        # only get information for these features
        feats = ['microscope setting', 'imager', 'date taken', 'date uploaded',
                 'release date']

        # Get an html string of descriptions for all images
        image_description_html = ''
        for img in images:
            image_description_html += su.image_details_to_html(img,
                img.medium_thumb.url, feats)
            image_description_html += "</br></br></br>"
        context['image_description_html'] = image_description_html

        return context

    def form_valid(self, form):
        experiment = form.save()
        return HttpResponseRedirect(reverse('images:experiment_details',
                                            args=(experiment.id,)))


class UpdateImageView(TemplateNames, genViews.UpdateView):
    model = models.Image
    form_class = forms.UpdateImageForm

    def get_object(self):
        try:
            # get the image
            img = models.Image.objects.get(pk=self.kwargs['pk'])
        # raise 404 if the image does not exist
        except models.Image.DoesNotExist:
            error = "Image with id {} does not exist.".format(
                self.kwargs['pk'])
            raise Http404(error)

        # raise permission denied if the image is not editable
        if not img.is_editable and not self.request.user.is_superuser:
            ud = img.date_uploaded
            pk = img.pk
            html = "<h2> Image Not Editable </h2> \
                <p>The allowed time to update or delete this image has passed.\
                The upload date for this image is {}. If you need to edit this \
                image, please contanct an admin and have them edit the image \
                with id {}.".format(ud, pk)
            html += "</br></br>"
            # include information on the image
            html += su.image_details_to_html(img, img.large_thumb.url)
            # TODO: include information on how the user can go about editing
            # this image
            raise PermissionDenied(html)
        else:
            return img

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


class MultipleImageUpdateView(TemplateNames, genViews.TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        errors = []
        image_pks_str = self.kwargs['list_image_pks']
        # convert string into list of numbers
        image_pks_str = image_pks_str.replace('[', '').replace(']', '')
        image_pks = []
        for ips in image_pks_str.split(', '):
            try:
                image_pks.append(int(ips))
            except Exception as e:
                print(e)
                errors.append(ips)

        by_experiment = {}
        for pk in image_pks:
            # get image or error
            img = models.Image.objects.filter(id=pk)
            # if img is empty list append pk onto errors
            if len(img) == 0:
                errors.append(pk)
                continue
            else:
                # image exists, take first and only one in query
                img = img[0]

            # get display information for image
            features = ['imager', 'description', 'microscope setting',
                        'file name', 'date taken', 'date uploaded',
                        'release date', 'raw data path']
            idict = {'details': su.get_html_image_list(img, features), 'pk': pk,
                     'thumb': img.medium_thumb.url, 'editable': img.is_editable}

            # sort it by experiment in case more than one appear here
            epk = img.experiment.pk
            # if the experiment doesn't exist, create new information for it
            if epk not in by_experiment.keys():
                by_experiment[epk] = {'pk': epk, 'image_info': [],
                    'name': img.experiment.name, 'experiment_details':
                    su.get_html_experiment_list(img.experiment), 'editable':
                    img.experiment.is_editable}

            # add image info to correct experiment
            by_experiment[epk]['image_info'].append(idict)

        # make variable to store the error images
        context['errors'] = errors

        # convert experiment dict to a list
        list_exps = []
        for key in by_experiment.keys():
            list_exps.append(by_experiment[key])

        # make context variable

        context['experiments'] = list_exps

        return context


###############################################################################
# DELETE VIEWS # DELETE VIEWS # DELETE VIEWS # DELETE VIEWS # DELETE VIEWS# DELE
###############################################################################
class DeleteImageView(TemplateNames, genViews.DeleteView):
    model = models.Image

    # need to use the method because using success_url = blah causes errors
    def get_success_url(self):
        return reverse('images:pick_experiment')

    def get_object(self):
        try:
            # get the image
            img = models.Image.objects.get(pk=self.kwargs['pk'])
        # raise 404 if the image does not exist
        except models.Image.DoesNotExist:
            error = "Image with id {} does not exist.".format(
                self.kwargs['pk'])
            raise Http404(error)

        # raise permission denied if the image is not editable
        if not img.is_editable:
                error = "Image with id {} cannot be deleted because it has \
                         been over a day since it was uploaded.".format(
                         self.kwargs['pk'])
                error += "</br></br>"
                # include information on the image
                error += su.image_details_to_html(img, img.large_thumb.url)
                # TODO: include information on how the user can go about editing
                # this image
                raise PermissionDenied(error)
        else:
            return img

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the image
        image = kwargs['object']
        # get the html string for image details
        context['image_details'] = su.image_details_to_html(image,
            image.large_thumb.url)
        return context


class DeleteExperimentView(TemplateNames, genViews.DeleteView):
    model = models.Experiment

    # need to use the method because using success_url = blah causes errors
    def get_success_url(self):
        return reverse('images:pick_experiment')

    def get_object(self):
        try:
            # get the image
            exp = models.Experiment.objects.get(pk=self.kwargs['pk'])
        # raise 404 if the image does not exist
        except models.Experiment.DoesNotExist:
            error = "Experiment with id {} does not exist.".format(
                self.kwargs['pk'])
            raise Http404(error)

        # raise permission denied if the image is not editable
        if not exp.is_editable:
                error = "Experiment with id {} cannot be deleted because it \
                         has been over a day since it was uploaded.".format(
                         self.kwargs['pk'])
                error += "</br></br>"
                # include information on the image
                #error += su.image_details_to_html(img, img.large_thumb.url)
                # TODO: include information on how the user can go about editing
                # this image
                raise PermissionDenied(error)
        else:
            return exp

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the experiment
        exp = kwargs['object']
        # get the experiment data
        context['get_experiment_details'] = su.get_html_experiment_list(exp)

        # get data for each image
        # not worrying about release date, because they are still within the
        # delete period
        imgs = exp.image_set.all()
        context['images'] = []
        for img in imgs:
            context['images'].append(su.image_details_to_html(img,
                img.medium_thumb.url, ['microscope setting', 'imager',
                'date taken', 'date uploaded', 'release date']))
        return context

    # TODO: Make this automic
    def delete(self, request, *args, **kwargs):
        # code needed from super delete method
        success_url = self.get_success_url()

        # not worried about if it exists or not, because that was already
        # checked when geting the object
        exp = models.Experiment.objects.get(pk=self.kwargs['pk'])

        try:
            with transaction.atomic():
                # delete all the associated images
                imgs = exp.image_set.all()
                for img in imgs:
                    img.delete()
                exp.delete()
                return HttpResponseRedirect(success_url)
        except Exception as e:
            # return with an error page if transaction doesn't fully complete
            context = {'error':  e}
            rendered = render_to_string('images_misc/failed_experiment_delete_view.html',
                                        context)
            return HttpResponse(rendered)
