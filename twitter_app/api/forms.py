from django import forms
from django.core.exceptions import ValidationError


class APIForm(forms.Form):
    term = forms.CharField(max_length=50,
                           widget=forms.TextInput(attrs={'placeholder': 'term', 'id': 'term'}))

    lang = forms.CharField(max_length=2, required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'language', 'id': 'lang'}))

    country = forms.CharField(max_length=50, required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'country', 'id': 'country'}))

    referenced_tweets = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'ref_tw'}))

    place = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'pace'}))

    source = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'source'}))

    num_tw = forms.CharField(required=True,
                             widget=forms.NumberInput({'placeholder': 'number of tweets', 'id': 'num_tw', 'min': 10, 'max': 10000}))

    priority = forms.CharField(required=True,
                               widget=forms.NumberInput(
                                   {'placeholder': 'priority between 1 and 5', 'id': 'num_tw', 'min': 1, 'max': 5}))

    def clean(self):
        clean_data = self.cleaned_data
        term_clean = self.cleaned_data.get('term').strip()
        str_aux = term_clean.replace(' ', '')
        lang_clean = self.cleaned_data.get('lang').strip()
        country_clean = self.cleaned_data.get('country').strip()
        num_tw_clean = self.cleaned_data.get('num_tw').strip()
        priority_clean = self.cleaned_data.get('priority').strip()

        if not priority_clean.isnumeric() and (1 <= priority_clean <= 5):
            raise forms.ValidationError({'num_tw': 'only can introduce digits and the digits must be between 1 and 5'})

        if not num_tw_clean.isnumeric():
            raise forms.ValidationError({'num_tw': 'only can introduce digits'})

        if not country_clean.isalpha():
            raise forms.ValidationError({'country': 'only can introduce chraracters'})

        if not str_aux.isalnum():
            raise forms.ValidationError({'term': 'only can introduce characters and digits'})

        if not lang_clean.isalpha():
            raise forms.ValidationError({'lang': 'lang code must have only two characters'})

        return clean_data


'''class SearchHomeForm(forms.Form):
    location = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': "Localidad", 'class': "input-field autocomplete ", 'id': "autocomplete-input"}))
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        ),
        input_formats=settings.DATE_INPUT_FORMATS
    )
    start_hour = forms.TimeField(
        required=False,
        widget=forms.TimeInput(
            format='%H:%M',
            attrs={'placeholder': "hh:mm"}
        ),
        input_formats=('%H:%M',)
    )
    latitude = forms.DecimalField(required=False, widget=forms.HiddenInput())
    longitude = forms.DecimalField(required=False, widget=forms.HiddenInput())

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < now().date():
            raise ValidationError(
                'La fecha debe ser futura')
        return date

    def clean_location(self):
        location = self.cleaned_data.get('location')
        location_join = location.replace(' ', '')
        if not location_join.isalpha() and location:
            raise ValidationError('Introduzca solo letras y espacios')
        return location'''
