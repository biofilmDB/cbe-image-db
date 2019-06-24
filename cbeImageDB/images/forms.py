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
        fields = ['document', 'date', 'imager', 'lab',
                  'brief_description', ]
        widgets = {
            'imager':
            autocomplete.ModelSelect2(url='/images/imager-autocomplete/'),
            'lab':
            autocomplete.ModelSelect2Multiple(url='/images/lab-autocomplete/'),
            'date':
            forms.SelectDateWidget()
        }


class SearchImageForm(forms.Form):
    select_a_lab = forms.ModelChoiceField(queryset=Lab.objects.all(),
        widget=autocomplete.ModelSelect2(url='/images/lab-autocomplete'))
