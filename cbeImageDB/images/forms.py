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
    yn = [('y', 'yes'), ('n', 'no')]
    organs = [('a', 'Organism A'), ('b', 'Organism B')]
    organism = forms.ChoiceField(choices=organs)

    growth_medium = forms.CharField()
    things = [('g', 'Glass'), ('b', 'Rope')]
    substratum = forms.ChoiceField(choices=things)
    reactors = [('a', 'Reactor A'), ('b', 'Reactor B')]
    reactor = forms.ChoiceField(choices=reactors)

    batch = forms.ChoiceField(choices=yn, required=False)
    batch_help_text = 'mL   (Field only required if slected yes for batch)'
    medium_volume = forms.FloatField(help_text=batch_help_text, required=False)
    gas_volume = forms.FloatField(help_text=batch_help_text, required=False)

    continuous = forms.ChoiceField(choices=yn)
    flow_rate = forms.FloatField(help_text='mL/hr (Field required only if yes selected for continuous)',
                                 required=False)
    dilution_rate = forms.FloatField(help_text='per hr (Field required only if yes selected for continuous)',
                                     required=False)
    aerobic = forms.ChoiceField(choices=yn)
    microaerophilic = forms.ChoiceField(choices=yn)
    gas_microaerophilic = forms.CharField(help_text='Field required only if yes to microaerophilic)',
                                          required=False)
    anoxic = forms.ChoiceField(choices=yn)
    gas_anoxic = forms.CharField(help_text='Field required only if yes to anoxic)',
                                 required=False)

    planktonic_cell_count = forms.FloatField(required=False)
    planktonic_protein = forms.FloatField(required=False)

    def fields_required(self, fields, selection):
        for field in fields:
            if not self.cleaned_data.get(field, ''):
                string = "{} is required due to {} selection.".format(
                    field.replace("_", ' '), selection)
                msg = forms.ValidationError(string)
                self.add_error(field, msg)

    def clean(self):
        batch = self.cleaned_data.get('batch')
        if batch == 'y':
            self.fields_required(['medium_volume', 'gas_volume'], 'batch')
        if self.cleaned_data.get('continuous') == 'y':
            self.fields_required(['flow_rate', 'dilution_rate'], 'continuous')
        if self.cleaned_data.get('microaerophilic') == 'y':
            self.fields_required(['gas_microaerophilic'], 'microaerophilic')
        if self.cleaned_data.get('anoxic') == 'y':
            self.fields_required(['gas_anoxic'], 'anoxic')

        return self.cleaned_data

    class Meta:
        model = Image
        fields = ['document', 'date_taken', 'imager', 'lab',
                  'microscope_setting', 'brief_description', ]
        widgets = {
            'imager':
            autocomplete.ModelSelect2(url='/images/imager-autocomplete/'),
            'lab':
            autocomplete.ModelSelect2Multiple(url='/images/lab-autocomplete/'),
            'microscope_setting':
            autocomplete.ModelSelect2(url='/images/microscope-setting-autocomplete/'),
            'date_taken':
            forms.SelectDateWidget()
        }


class GeneralSearchImageForm(forms.Form):
    search = forms.MultipleChoiceField(
        widget=autocomplete.Select2Multiple('/images/search-autocomplete'))


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
    day_taken = forms.ChoiceField(required=False,
        widget=autocomplete.ListSelect2('/images/day-autocomplete'))
    month_taken = forms.ChoiceField(required=False,
        widget=autocomplete.ListSelect2('/images/month-autocomplete'))
    year_taken = forms.ChoiceField(required=False,
        widget=autocomplete.ListSelect2('/images/year-autocomplete'))
