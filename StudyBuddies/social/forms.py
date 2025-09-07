from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError


class SearchForm(forms.Form):
    SEARCH_CHOICES = (('users', 'Users'), ('groups', 'Groups'))
    search_string = forms.CharField(label="Cerca", max_length=100, required=True)
    search_from=forms.ChoiceField(choices=SEARCH_CHOICES, label="cosa cercare", widget=forms.Select(attrs={'class':'form-select'}))
  