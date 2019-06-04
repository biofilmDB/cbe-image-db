from django import forms
from .models import Image, Lab


class UploadFileForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['document', 'lab', 'brief_description', ]


class SearchImageForm(forms.Form):
    opts = ()
    for lab in Lab.objects.all():
        opts = opts + ((lab, lab), )
    selected_labs = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=opts)
    selected_labs = forms.ModelChoiceField(queryset=Lab.objects,
        empty_label="(-----")
