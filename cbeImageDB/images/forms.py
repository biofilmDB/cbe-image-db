from django import forms
from .models import Image, Lab, Imager
from dal import autocomplete


class AddImagerForm(forms.ModelForm):

    class Meta:
        model = Imager
        fields = ['imager_name', ]


class UploadFileForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['document', 'imager', 'lab', 'brief_description', ]
        widgets = {
            'imager':
            autocomplete.ModelSelect2(url='imager_autocomplete/')
        }

class SearchImageForm(forms.Form):
    select_a_lab = forms.ModelChoiceField(queryset=Lab.objects,
                                          empty_label="-----------")
