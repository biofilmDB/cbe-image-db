from django import forms
from .models import Image, Lab


class UploadFileForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['document', 'lab', 'brief_description', ]


class SearchImageForm(forms.Form):
    select_a_lab = forms.ModelChoiceField(queryset=Lab.objects,
                                          empty_label="-----------")
