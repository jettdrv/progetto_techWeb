from django import forms
from .models import StudySession, Subject
from django.utils import timezone
from django.core.exceptions import ValidationError

#ModelForm per permettere all'utente di inserire o modificare i dati della tabella delle sessioni di studio - form identico a una tabella di database
class CreateSessionForm(forms.ModelForm):
    
    #form per l'aggiunta di una nuova materia. L'utente può scegliere tra quelle esistenti o aggiungerne una nuova
    subject_input = forms.CharField(max_length=50, required=False, label="oppure inserisci una nuova materia")
    class Meta:
        model = StudySession
        fields = ('subject', 'subject_input', 'duration', 'date', 'notes')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'max': timezone.now().date()}),
            'duration': forms.NumberInput(attrs={'step': '0.5', 'min': '0.5', 'max': '24'}),
            'subject': forms.Select(attrs={'class':'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'subject': 'Materia',
            'duration': 'Durata (ore)',
            'date': 'Data',
            'notes': 'Note',
        }
        
        
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user=user
        self.fields['subject'].queryset = Subject.objects.filter(created_by=user)
        self.fields['subject'].required = False
        self.fields['subject'].empty_label = "Seleziona una materia"


    def clean(self):
        cleaned_data = super().clean()
        subject = cleaned_data.get('subject')
        new_subject = cleaned_data.get('subject_input')
    
        if not subject and not new_subject:
            raise ValidationError("Devi selezionare una materia esistente o inserirne una nuova.")

        if subject and new_subject:
            raise ValidationError("Seleziona una materia esistente O inserisci una nuova materia, non entrambi.")
 
        if new_subject and not new_subject.strip():
            raise ValidationError("Il nome della nuova materia non può essere vuoto.")
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        new_subject_name = self.cleaned_data.get('subject_input')
        if new_subject_name:
            new_subject_name = new_subject_name.strip()
            existing_subject = Subject.objects.filter(name__iexact=new_subject_name).first()
            if existing_subject:
                instance.subject = existing_subject
            else:
                new_subject = Subject.objects.create(
                    name=new_subject_name,
                    created_by=instance.user
                )
                instance.subject = new_subject
    
        if commit:
            instance.save()
        return instance
