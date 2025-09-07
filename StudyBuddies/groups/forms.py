from django import forms
from .models import StudyGroup, GroupDiscussion, Comment, GroupInvite
from django.contrib.auth import get_user_model

User = get_user_model()

class StudyGroupForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ['name', 'description', 'privacy']

class GroupDiscussionForm(forms.ModelForm):
    class Meta:
        model = GroupDiscussion
        fields = ['content']
        widgets =  {'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Fai una domanda... '})}

class CommentForm(forms.ModelForm):
    class Meta:
        model= Comment
        fields = ['content']
        widgets =  {'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Rispondi... '})}

class GroupInviteForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Username dell'utente da invitare", widget=forms.TextInput(attrs={
            'class': 'form-control',
        }))
    class Meta:
        model = GroupInvite
        fields = []
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('Utente non trovato')
        return user