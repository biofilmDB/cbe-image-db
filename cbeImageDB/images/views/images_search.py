from images import forms, models
import django.views.generic as genViews
from dal import autocomplete
from django.utils.datastructures import MultiValueDictKeyError
from template_names import TemplateNames
from images import search_utils as su
from datetime import datetime
from images.documents import ImageDocument


def get_description_search_qs(request, qs):
    exist = False
    try:
        desct = request.GET.get('description_search')
        if desct != '':
            s = ImageDocument.search().query("match", brief_description=desct)
            qs = qs & s.to_queryset()
            exist = True

    except MultiValueDictKeyError:
        pass
    return qs, exist


# Search all searchable terms at the same time
class GeneralSearchView(genViews.FormView):
    form_class = forms.GeneralSearchImageForm
    template_name = 'images_search/search_images.html'


class GeneralSearchResultsView(genViews.ListView):
    model = models.Image
    context_object_name = 'image_list'
    template_name = 'images_search/image_search_results.html'
    paginate_by = 5
    features = []

    def get_queryset(self):
        if self.request.user.is_superuser:
            qs = models.Image.objects.all()
        else:
            qs = models.Image.objects.filter(release_date__lte=datetime.now())
        features = ['search', 'lab']
        try:
            search_list = self.request.GET.getlist('search')
            for search in search_list:
                q = search.split(': ')
                q2 = ': '.join(q[1:])
                if q[0].lower() == 'imager':
                    features.append('imager')
                    qs = qs.filter(imager__imager_name=q2)

                elif q[0].lower() == 'objective medium':
                    qs = qs.filter(microscope_setting__medium__medium_type=q2)

                elif q[0].lower() == 'objective':
                    # remove x from objective
                    obj = float(q[-1][:-1])
                    qs = qs.filter(microscope_setting__objective=obj)

                elif q[0].lower() == 'microscope':
                    qs = qs.filter(microscope_setting__microscope__microscope_name=q2)
                elif q[0].lower() == 'day':
                    features.append('date_taken')
                    qs = qs.filter(date_taken__day=q2)
                elif q[0].lower() == 'month':
                    features.append('date_taken')
                    month = su.month_string_to_int(q2)
                    qs = qs.filter(date_taken__month=month)
                elif q[0].lower() == 'year':
                    features.append('date_taken')
                    qs = qs.filter(date_taken__year=q2)
                # Experiment values
                elif q[0].lower() == 'project':
                    features.append('project')
                    qs = qs.filter(experiment__project__name=q2)
                elif q[0].lower() == 'lab':
                    print('looking kup a lab {}'.format(q2))
                    qs = qs.filter(experiment__lab__pi_name=q2)
                elif q[0].lower() == 'organism':
                    qs = qs.filter(experiment__organism__organism_name=q2)
                elif q[0].lower() == 'vessel':
                    features.append('vessel')
                    qs = qs.filter(experiment__vessel__name=q2)
                elif q[0].lower() == 'growth medium':
                    features.append('growth medium')
                    qs = qs.filter(experiment__growth_medium__growth_medium=q2)
                elif q[0].lower() == 'growth substratum':
                    features.append('growth substratum')
                    qs = qs.filter(experiment__substratum__substratum=q2)

        except MultiValueDictKeyError:
            pass

        qs, exists = get_description_search_qs(self.request, qs)
        if exists:
            features.append('description')

        self.features = features

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['features'] = self.features
        context['get_image_details'] = []
        if len(context['image_list']) > 0:
            for image in context['image_list']:
                t = su.get_html_image_dict(image, self.features)
                context['get_image_details'].append(t)
        return context


# Search by attributes
class AttributeSearchImageView(TemplateNames, genViews.FormView):
    """ Allows the users to search images by selecting criteria for attributes
    of the image"""
    form_class = forms.AttributeSearchImageForm


class AttributeSearchResultsView(genViews.ListView):
    """ Shows all of the images that match a search criteria."""
    model = models.Image
    context_object_name = 'image_list'
    template_name = 'images_search/image_search_results.html'
    paginate_by = 5
    features = []

    def get_queryset(self):
        if self.request.user.is_superuser:
            qs = models.Image.objects.all()
        else:
            qs = models.Image.objects.filter(release_date__lte=datetime.now())

        features = ['search', 'lab']
        # Variable to tell if there was something that was searched
        try:
            search_lab = self.request.GET['lab']
            if search_lab != '':
                qs = qs.filter(experiment__lab=search_lab)
        except MultiValueDictKeyError:
            pass

        try:
            search_imager = self.request.GET['imager']
            if search_imager != '':
                features.append('imager')
                qs = qs.filter(imager=search_imager)
        except MultiValueDictKeyError:
            pass

        try:
            search_objective = self.request.GET['objective']
            if search_objective != '':
                qs = qs.filter(microscope_setting__objective=search_objective)

        except MultiValueDictKeyError:
            pass

        try:
            microscope = self.request.GET['microscope']
            if microscope != '':
                qs = qs.filter(microscope_setting__microscope=microscope)
        except MultiValueDictKeyError:
            pass

        try:
            obj_medium = self.request.GET['objective_medium']
            if obj_medium != '':
                qs = qs.filter(microscope_setting__medium=obj_medium)
        except MultiValueDictKeyError:
            pass

        try:
            day = self.request.GET['day_taken']
            if day != '':
                features.append('date taken')
                qs = qs.filter(date_taken__day=day)
        except MultiValueDictKeyError:
            pass

        try:
            month = self.request.GET['month_taken']
            if month != '':
                features.append('date taken')
                month = su.month_string_to_int(month)
                qs = qs.filter(date_taken__month=month)
        except MultiValueDictKeyError:
            pass

        try:
            year = self.request.GET['year_taken']
            if year != '':
                features.append('date taken')
                qs = qs.filter(date_taken__year=year)
        except MultiValueDictKeyError:
            pass

        try:
            organ = self.request.GET['organism']
            if organ != '':
                qs = qs.filter(experiment__organism=organ)
        except MultiValueDictKeyError:
            pass

        try:
            v = self.request.GET['vessel']
            if v != '':
                features.append('vessel')
                qs = qs.filter(experiment__vessel=v)
        except MultiValueDictKeyError:
            pass

        try:
            v = self.request.GET['growth_medium']
            if v != '':
                features.append('growth medium')
                qs = qs.filter(experiment__growth_medium=v)
        except MultiValueDictKeyError:
            pass

        try:
            v = self.request.GET['growth_substratum']
            if v != '':
                features.append('growth substratum')
                qs = qs.filter(experiment__substratum=v)
        except MultiValueDictKeyError:
            pass

        try:
            v = self.request.GET['project']
            if v != '':
                features.append('project')
                qs = qs.filter(experiment__project=v)
        except MultiValueDictKeyError:
            pass

        qs, exists = get_description_search_qs(self.request, qs)
        if exists:
            features.append('description')

        self.features = features

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['get_image_details'] = []
        for image in context['image_list']:
            t = su.get_html_image_dict(image, self.features)
            context['get_image_details'].append(t)
        return context


# Where is the correct location for this? Here or autocomplete?
class SearchAutocomplete(autocomplete.Select2ListView):

    def get_list(self):
        search_terms = ['Lab: ' + str(x) for x in list(models.Lab.objects.all())]
        search_terms.extend(['Project: ' + str(x) for x in models.Project.objects.all()])
        search_terms.extend(['Imager: ' + str(x) for x in
                            list(models.Imager.objects.all())])
        search_terms.extend(['Microscope: ' + str(x) for x in
                            list(models.Microscope.objects.all())])
        search_terms.extend(['Objective Medium: ' + str(x) for x in
                             list(models.ObjectiveMedium.objects.all())])
        search_terms.extend(['Objective: ' + x for x in su.get_objectives()])
        search_terms.extend(['Organism: ' + x for x in su.get_organism_list()])
        search_terms.extend(['Vessel: ' + str(x) for x in models.Vessel.objects.all()])
        search_terms.extend(['Growth Medium: ' + str(x) for x in
                             models.GrowthMedium.objects.all()])
        search_terms.extend(['Growth Substriatum: ' + str(x) for x in
                             models.GrowthSubstratum.objects.all()])
        search_terms.extend(['Day: ' + str(x) for x in range(1, 32)])
        months = ['January', 'Febuary', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November',
                  'December']
        search_terms.extend(['Month: ' + x for x in months])
        search_terms.extend(['Year: ' + str(x) for x in su.get_year_list()])
        return search_terms
