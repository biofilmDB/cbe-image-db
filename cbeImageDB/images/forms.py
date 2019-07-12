from django import forms
from .models import Image, Lab, Imager, Microscope, Medium
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
            autocomplete.ModelSelect2(url='/images/microscope-setting-autocomplete/'),
            'date':
            forms.SelectDateWidget()
        }


class GeneralSearchImageForm(forms.Form):
    search = forms.MultipleChoiceField(
        widget=autocomplete.Select2Multiple('/images/search-autocomplete'))

def get_months():
    months = ['January', 'Febuary', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November',
                'December']
    months_tuples = []
    for m in months:
        months_tuples.append((m, m))
    return months


class AttributeSearchImageForm(forms.Form):
    lab = forms.ModelChoiceField(queryset=Lab.objects.all(), required=False,
        widget=autocomplete.ModelSelect2(url='/images/lab-autocomplete'))
    imager = forms.ModelChoiceField(queryset=Imager.objects.all(), required=False,
        widget=autocomplete.ModelSelect2(url='/images/imager-autocomplete'))
    microscope = forms.ModelChoiceField(queryset=Microscope.objects.all(),
        required=False, widget=autocomplete.ModelSelect2(url='/images/microscope-autocomplete'))
    objective = forms.FloatField(required=False)
    objective_medium = forms.ModelChoiceField(queryset=Medium.objects.all(), required=False,
        widget=autocomplete.ModelSelect2(url='/images/medium-autocomplete'))
    day = forms.IntegerField(required=False)
    month = forms.ChoiceField(required=False,
        widget=autocomplete.ListSelect2('/images/month-autocomplete'))
    year = forms.IntegerField(required=False)

    # TODO: Not being called, becuase using a GET request, figure out a way to
    # validate day and year fields
    def clean_day(self):
        data = self.cleaned_data['day']
        import pdb; pdb.set_trace()
        if data < 1 or data > 31:
            raise forms.ValidationError("Invalid day")
        else:
            return data

