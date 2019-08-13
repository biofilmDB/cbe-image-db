from django import forms
from .models import Image, Lab, Imager, Microscope, Medium, Organism
from dal import autocomplete


class AddImagerForm(forms.ModelForm):

    class Meta:
        model = Imager
        fields = ['imager_name', ]

    def clean_imager_name(self):
        data = self.cleaned_data['imager_name']
        query = Imager.objects.filter(imager_name__iexact=data)
        if len(query) > 0:
            raise forms.ValidationError("{} already exists, try again".format(data))
        else:
            return data


class UploadFileForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['document', 'date_taken', 'release_date', 'imager', 'lab',
                  'organism', 'microscope_setting', 'brief_description', ]
        help_texts = {
            'brief_description': '1000 character max overview of the project',
        }
        widgets = {
            'imager':
            autocomplete.ModelSelect2(url='/images/add-imager-autocomplete/'),
            'lab':
            autocomplete.ModelSelect2Multiple(url='/images/lab-autocomplete/'),
            'organism':
            autocomplete.ModelSelect2Multiple(url='/images/organism-autocomplete/'),
            'microscope_setting':
            autocomplete.ModelSelect2(url='/images/microscope-setting-autocomplete/'),
            'date_taken':
            forms.SelectDateWidget(),
            'release_date':
            forms.SelectDateWidget()
        }


class GeneralSearchImageForm(forms.Form):
    search = forms.MultipleChoiceField(
        widget=autocomplete.Select2Multiple('/images/search-autocomplete'),
                                            required=False)
    description_search = forms.CharField(required=False)


class AttributeSearchImageForm(forms.Form):
    lab = forms.ModelChoiceField(queryset=Lab.objects.all(), required=False,
        widget=autocomplete.ModelSelect2(url='/images/lab-autocomplete'))
    imager = forms.ModelChoiceField(queryset=Imager.objects.all(), required=False,
        widget=autocomplete.ModelSelect2(url='/images/imager-autocomplete'))
    organism = forms.ModelChoiceField(queryset=Organism.objects.all(), required=False,
        widget=autocomplete.ModelSelect2(url='/images/organism-autocomplete'))
    description_search = forms.CharField(required=False)
    microscope = forms.ModelChoiceField(queryset=Microscope.objects.all(),
        required=False, widget=autocomplete.ModelSelect2(url='/images/microscope-autocomplete'))
    objective = forms.FloatField(required=False)
    objective_medium = forms.ModelChoiceField(queryset=Medium.objects.all(), required=False,
        widget=autocomplete.ModelSelect2(url='/images/medium-autocomplete'))
    day_taken = forms.ChoiceField(required=False,
        widget=autocomplete.ListSelect2('/images/day-autocomplete'))
    month_taken = forms.ChoiceField(required=False,
        widget=autocomplete.ListSelect2('/images/month-autocomplete'))
    year_taken = forms.ChoiceField(required=False,
        widget=autocomplete.ListSelect2('/images/year-autocomplete'))
