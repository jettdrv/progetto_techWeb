from django import forms
from .models import StudySession
from django.utils import timezone

#ModelForm per permettere all'utente di inserire o modificare i dati della tabella delle sessioni di studio - form identico a una tabella di database
class CreateSessionForm(forms.ModelForm):
    
    class Meta:
        model = StudySession
        fields = ('subject', 'duration', 'date', 'notes')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'max': timezone.now().date()}),
            'duration': forms.NumberInput(attrs={'step': '0.5', 'min': '0.5', 'max': '24'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'subject': 'Materia',
            'duration': 'Durata (ore)',
            'date': 'Data',
            'notes': 'Note',
        }
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['subject'].queryset = Subject.objects.all().order_by('name')

'''
class StudySessionForm(forms.ModelForm):
    class Meta:
        model = StudySession
        fields = ['subject', 'duration', 'date', 'notes']
        
'''
   