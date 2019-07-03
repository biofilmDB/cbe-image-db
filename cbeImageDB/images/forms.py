from django import forms
from .models import Image, Lab, Imager
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
        fields = ['document', 'date', 'imager', 'lab', 'microscope_setting',
                  'brief_description', ]
        widgets = {
            'imager':
            autocomplete.ModelSelect2(url='/images/imager-autocomplete/'),
            'lab':
            autocomplete.ModelSelect2Multiple(url='/images/lab-autocomplete/'),
            'microscope_setting':
            autocomplete.ModelSelect2(url='/images/microscope-autocomplete/'),
            'date':
            forms.SelectDateWidget()
        }


class GeneralSearchImageForm(forms.Form):
    search = forms.MultipleChoiceField(
        widget=autocomplete.Select2Multiple('/images/search-autocomplete'))


class AttributeSearchImageForm(forms.Form):
    search_lab = forms.ModelChoiceField(queryset=Lab.objects.all(), required=False,
        widget=autocomplete.ModelSelect2(url='/images/lab-autocomplete'))
    search_imager = forms.ModelChoiceField(queryset=Imager.objects.all(), required=False,
        widget=autocomplete.ModelSelect2(url='/images/imager-autocomplete'))
    search_objective = forms.FloatField(required=False)
