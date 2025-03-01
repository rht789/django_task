from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','password2','email']
        
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            
class CustomRegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','password2','email']
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not password1:
            raise forms.ValidationError("Password is required.")
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isupper() for char in password1):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError("Password must contain at least one number.")
        if not any(char in '!@#$%^&*()' for char in password1):
            raise forms.ValidationError("Password must contain at least one special character (e.g., !@#$%^&*()).")
        return password1