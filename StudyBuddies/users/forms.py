from django import forms 
from django.forms import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model= CustomUser
        fields= ['username', 'email', 'user_type', 'expertise_field', 'password1', 'password2']
    
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expertise_field'].required = False

class GoalSettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['daily_goal_hours', 'weekly_goal_hours']
        labels = {'daily_goal_hours': 'Obiettivo giornaliero', 'weekly_goal_hours': 'Obiettivo settimanale'}

        widgets = {'daily_goal_hours': forms.NumberInput(attrs={'step': '0.5', 'min': '0.0', 'max': '24'}), 'weekly_goal_hours': forms.NumberInput(attrs={'step': '1', 'min': '0.0', 'max': '168'})}   

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']
        widgets = {
            'profile_picture' : forms.FileInput(attrs={
                'accept':'image.*',
                'class': 'form-control'
            })
        }

    def control_pfp(self):
        image = self.cleaned_data.get('profile_picture')
        if image:
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if image.content_type not in allowed_types:
                raise ValidationError("Formato non supportato. ")
        return image
