from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import Group, Permission
from tasks.forms import StyledFormMixin
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()


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
    
class LoginForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
    
class AssignRoleForm(StyledFormMixin, forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a role"
    )

class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign Permission"
    )
    
    class Meta:
        model = Group
        fields = ['name', 'permissions']
    
class CustomPasswordChangeForm(StyledFormMixin,PasswordChangeForm):
    pass
class CustomPasswordResetForm(StyledFormMixin,PasswordResetForm):
    pass
class CustomPasswordResetConfirmForm(StyledFormMixin,SetPasswordForm):
    pass
"""
class EditProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    bio = forms.CharField(required=False, widget=forms.Textarea, label='Bio')
    profile_image = forms.ImageField(required=False, label='Profile Image')

    def __init__(self, *args, **kwargs):
        self.userprofile = kwargs.pop('userprofile', None)
        super().__init__(*args, **kwargs)
        print("forms", self.userprofile)

        # Todo: Handle Error

        if self.userprofile:
            self.fields['bio'].initial = self.userprofile.bio
            self.fields['profile_image'].initial = self.userprofile.profile_image

    def save(self, commit=True):
        user = super().save(commit=False)

        # Save userProfile jodi thake
        if self.userprofile:
            self.userprofile.bio = self.cleaned_data.get('bio')
            self.userprofile.profile_image = self.cleaned_data.get(
                'profile_image')

            if commit:
                self.userprofile.save()

        if commit:
            user.save()

        return user
"""
    
class EditProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'bio', 'profile_image']