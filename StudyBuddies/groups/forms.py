from django import forms
from .models import StudyGroup, GroupDiscussion, Comment

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