from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from tasks.forms import StyledFormMixin

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','password2','email']
        
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            
class CustomRegisterForm(StyledFormMixin,forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','password2','email']

        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if not email:
            raise forms.ValidationError("Email is required.")
        
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("This email is already associated with an accont")
        return email
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if not username:
            raise forms.ValidationError("Username is required.")
        
        if User.objects.filter(username = username).exists():
            raise forms.ValidationError("Username already Exists")
        return username
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errors = []
        if not password1:
            errors.append("Password is required.")
        if len(password1) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not any(char.isupper() for char in password1):
            errors.append("Password must contain at least one uppercase letter.")
        if not any(char.isdigit() for char in password1):
            errors.append("Password must contain at least one number.")
        if not any(char in '!@#$%^&*()' for char in password1):
            errors.append("Password must contain at least one special character (e.g., !@#$%^&*()).")
        if errors:
            raise forms.ValidationError(errors)
        return password1
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password1')
        
        if password1 and password2 and password1!= password2:
            raise forms.ValidationError("Password Do Not Match")
        return cleaned_data
    
class AssignRoleForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a role"
    )