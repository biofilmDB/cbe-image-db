from django import forms
from .models import Image


class UploadFileForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['document', 'lab', ]
