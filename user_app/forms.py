from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Custom registration form
class CustomRegistrationForm(UserCreationForm):
    
    email = forms.EmailField()
    
    # Konfigurasi form
    class Meta:
        
        model = User

        fields = ['username', 'email', 'password1', 'password2']