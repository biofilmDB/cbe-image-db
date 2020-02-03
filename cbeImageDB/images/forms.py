from django import forms
from .models import Image, Lab, Imager, Microscope, ObjectiveMedium, Organism, Experiment
from .models import Project, GrowthSubstratum, Vessel
from images import help_texts as ht
from dal import autocomplete


def popover_html2(label, content):
    return label + ' <a tabindex="0" role="button" data-toggle="popover" data-html="true" \
            data-trigger="hover" data-placement="auto" data-content="{}"> \
            <span class="glyphicon glyphicon-info-sign"></span></a>'.format(content)

def popover_html(label, content):
    html = ' <a data-toggle="tooltip" title="{}">'.format(content)
    html += '<span class="glyphicon glyphicon-info-sign"></span></a> '
    return html + label

class CreateExperimentForm(forms.ModelForm):

    class Meta:
        model = Experiment
        fields = ['name', 'project', 'lab', 'organism', 'vessel',
                  'substratum',]
        labels = {
            'name': popover_html('Experiment Name', ht.experiment_name),
            'project': popover_html('Project', ht.experiment_project),
            'lab': popover_html('Lab(s)', ht.experiment_lab),
            'organism': popover_html('Organism(s)', ht.experiment_organism),
            'vessel': popover_html('Vessel', ht.experiment_vessel),
            'substratum': popover_html('Substratum', ht.experiment_substratum),
        }
        help_texts = {
            'name': '(500 character max)',
        }
        widgets = {
            'lab':
            autocomplete.ModelSelect2Multiple(url='/images/lab-autocomplete/'),
            'organism':
            autocomplete.ModelSelect2Multiple(url='/images/organism-autocomplete/'),
            'project':
            autocomplete.ModelSelect2(url='/images/add-project-autocomplete/'),
            'vessel':
            autocomplete.ModelSelect2(url='/images/vessel-autocomplete/'),
            'substratum':
            autocomplete.ModelSelect2(url='/images/growthsubstratum-autocomplete/'),
        }


class UploadFileForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['document', 'date_taken', 'release_date', 'imager',
                  'microscope_setting', 'brief_description',
                  'path_to_raw_data']

        labels = {
            'document': popover_html('Image File', ht.image_document),
            'date_taken': popover_html('Date Taken', ht.image_date_taken),
            'release_date': popover_html("Can't be used before",
                                         ht.image_release_date),
            'imager': popover_html('Imager', ht.image_imager),
            'microscope_setting': popover_html('Microscope Settings',
                                               ht.image_microscope_setting),
            'brief_description': popover_html('Brief Description',
                                              ht.image_breif_description),
            'path_to_raw_data': popover_html('Raw Data Location',
                                             ht.image_raw_data_location),
        }
        help_texts = {
            'brief_description': '(1000 character max)',
            'path_to_raw_data': '(500 character max)',
        }

        widgets = {
            'imager':
            autocomplete.ModelSelect2(url='/images/add-imager-autocomplete/'),
            'microscope_setting':
            autocomplete.ModelSelect2(url='/images/microscope-setting-autocomplete/'),
            'date_taken':
            forms.SelectDateWidget(),
            'release_date':
            forms.SelectDateWidget(),
        }


class ExperimentSearchForm(forms.Form):
    experiment_name = forms.CharField()


class GeneralSearchImageForm(forms.Form):
    search = forms.MultipleChoiceField(
        widget=autocomplete.Select2Multiple('/images/search-autocomplete'),
                                            required=False)
    description_search = forms.CharField(required=False)


class AttributeSearchImageForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), required=False,
        widget=autocomplete.ModelSelect2(url='/images/project-autocomplete'))
    lab = forms.ModelChoiceField(queryset=Lab.objects.all(), required=False,
        widget=autocomplete.ModelSelect2(url='/images/lab-autocomplete'))
    imager = forms.ModelChoiceField(queryset=Imager.objects.all(), required=False,
        widget=autocomplete.ModelSelect2(url='/images/imager-autocomplete'))
    organism = forms.ModelChoiceField(queryset=Organism.objects.all(), required=False,
        widget=autocomplete.ModelSelect2(url='/images/organism-autocomplete'))
    description_search = forms.CharField(required=False)
    vessel = forms.ModelChoiceField(queryset=Vessel.objects.all(), required=False,
        widget=autocomplete.ModelSelect2(url='/images/vessel-autocomplete'))
    growth_substratum = forms.ModelChoiceField(queryset=GrowthSubstratum.objects.all(),
        required=False, widget=autocomplete.ModelSelect2(url='/images/growthsubstratum-autocomplete'))
    microscope = forms.ModelChoiceField(queryset=Microscope.objects.all(),
        required=False, widget=autocomplete.ModelSelect2(url='/images/microscope-autocomplete'))
    objective = forms.FloatField(required=False)
    objective_medium = forms.ModelChoiceField(queryset=ObjectiveMedium.objects.all(), required=False,
        widget=autocomplete.ModelSelect2(url='/images/objectivemedium-autocomplete'))
    day_taken = forms.ChoiceField(required=False,
        widget=autocomplete.ListSelect2('/images/day-autocomplete'))
    month_taken = forms.ChoiceField(required=False,
        widget=autocomplete.ListSelect2('/images/month-autocomplete'))
    year_taken = forms.ChoiceField(required=False,
        widget=autocomplete.ListSelect2('/images/year-autocomplete'))
