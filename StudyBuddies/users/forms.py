from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model= CustomUser
        fields= ['username', 'email', 'user_type', 'expertise_field', 'password1', 'password2']
    
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expertise_field'].required = False
        '''
        self.fields['username'].widget.attrs.update({'placeholder': 'Scegli un username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'La tua email'})
        self.fields['expertise_field'].widget.attrs.update({'placeholder': 'Es: Informatica, Medicina, etc. (solo per professionisti)'})
        '''

#class CustomAuthenticationForm(AuthenticationForm):
