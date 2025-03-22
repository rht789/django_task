Below is your provided notes on **Customizing User Profile** in Django, organized into a detailed, structured format with expanded explanations for clarity. I’ve included emojis, code snippets, and thorough descriptions to ensure a beginner can understand the related code. Additionally, I’ve enhanced **17.6 Admin Panel Customization** with more information based on the code provided.

---

# **Module 17: Customizing User Profile**

This module covers how to extend and customize the Django user profile by adding fields like bio and profile image. We’ll explore two approaches: creating a separate `UserProfile` model with a one-to-one relationship and customizing the built-in `User` model. We’ll also fix errors and customize the admin panel for a better experience.

---

## **17.1 🌟 Create User Profile**

### **Why Extend the User Profile?**
- Django’s default `User` model (from `django.contrib.auth.models`) includes basic fields like `username`, `email`, and `password`. To add custom fields (e.g., `bio`, `profile_image`), we can either extend it with a related model or replace it entirely.

### **Approach 1: Separate UserProfile Model**
#### **models.py**
```python
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='userprofile', 
        primary_key=True
    )
    profile_image = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} profile'
```
#### **signals.py**
```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:  # Only run when a new User is created
        UserProfile.objects.create(user=instance)
```
- **Detailed Explanation** ✅  
  - **`UserProfile` Model**:  
    - `user = models.OneToOneField(...)`: Links each `UserProfile` to exactly one `User`. `on_delete=models.CASCADE` deletes the profile if the user is deleted. `related_name='userprofile'` lets us access it as `user.userprofile`. `primary_key=True` uses the user’s ID as the profile’s ID.  
    - `profile_image`: Stores an image in the `profile_images/` directory. `blank=True` makes it optional. Requires `Pillow` (`pip install Pillow`) and `MEDIA_ROOT`/`MEDIA_URL` in `settings.py`.  
    - `bio`: A text field for a user’s bio, also optional.  
    - `__str__`: Returns a readable string (e.g., “john_doe profile”).  
  - **Signals**:  
    - `@receiver(post_save, sender=User)`: Listens for the `post_save` signal, triggered when a `User` is saved.  
    - `if created`: Checks if the `User` is new (not updated). If true, creates a `UserProfile` linked to that user.  
    - **Purpose**: Automatically creates a profile for every new user.  
  - **Migration Issue**: After running `python manage.py makemigrations` and `migrate`, existing users (created before this model) lack a `UserProfile`, causing errors when accessing `user.userprofile`.

---

## **17.2 🛠️ Fixing the User Profile Error**

### **The Problem**
- Existing users don’t have a `UserProfile` because the model was added after they were created, leading to `AttributeError: 'User' object has no attribute 'userprofile'`.

### **Solution: Shell Script**
#### **Shell Command**
```python
# Run in python manage.py shell
from django.contrib.auth.models import User
from yourapp.models import UserProfile

users = User.objects.all()
for user in users:
    if not hasattr(user, 'userprofile'):  # Check if profile exists
        UserProfile.objects.create(user=user)
        print("Missing profile created for user:", user.username)
```
#### **admin.py**
```python
from django.contrib import admin
from .models import UserProfile

admin.site.register(UserProfile)  # Register UserProfile in admin
```
- **Detailed Explanation** ✅  
  - **Shell Script**:  
    - `users = User.objects.all()`: Fetches all users from the database.  
    - `hasattr(user, 'userprofile')`: Checks if the `userprofile` attribute exists (via the `related_name`).  
    - `UserProfile.objects.create(user=user)`: Creates a blank `UserProfile` for users missing one.  
    - `print(...)`: Confirms each fix (e.g., “Missing profile created for user: john_doe”).  
    - **Run**: Open the shell with `python manage.py shell`, paste, and execute.  
  - **`admin.site.register(UserProfile)`**: Adds `UserProfile` to the Django admin interface, letting admins view/edit profiles. Without this, it’s hidden.  
  - **Result**: All users now have a `UserProfile`, fixing the error.

---

## **17.3 ✏️ Edit User Profile**

### **Why Edit?**
- Users need to update their profile (e.g., email, name, bio, image). We’ll use a form and `UpdateView` to handle this.

#### **forms.py**
```python
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from .mixins import StyledFormMixin  # Assumed styling mixin

class EditProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    bio = forms.CharField(required=False, widget=forms.Textarea, label='Bio')
    profile_image = forms.ImageField(required=False, label='Profile Image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.userprofile:  # Set initial values from UserProfile
            self.fields['bio'].initial = self.userprofile.bio
            self.fields['profile_image'].initial = self.userprofile.profile_image

    def save(self, commit=True):
        user = super().save(commit=False)  # Save User fields
        if self.userprofile:  # Update UserProfile fields
            self.userprofile.bio = self.cleaned_data.get('bio')
            self.userprofile.profile_image = self.cleaned_data.get('profile_image')
            if commit:
                self.userprofile.save()
        if commit:
            user.save()
        return user
```
#### **views.py**
```python
from django.views.generic.edit import UpdateView
from django.shortcuts import redirect
from .forms import EditProfileForm
from .models import UserProfile

class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):  # Use current user
        return self.request.user

    def get_form_kwargs(self):  # Pass UserProfile to form
        kwargs = super().get_form_kwargs()
        kwargs['userprofile'] = UserProfile.objects.get(user=self.request.user)
        return kwargs

    def get_context_data(self, **kwargs):  # Pass form to template
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        context['form'] = self.form_class(instance=self.object, userprofile=user_profile)
        return context

    def form_valid(self, form):  # Save and redirect
        form.save(commit=True)
        return redirect('profile')
```
#### **urls.py**
```python
from django.urls import path
from .views import EditProfileView

urlpatterns = [
    path('edit-profile/', EditProfileView.as_view(), name='edit-profile'),
]
```
#### **Template: `accounts/update_profile.html`**
```html
{% extends "base.html" %}
{% block content %}
    <div class='mx-auto w-1/2 my-9'>
        {% if messages %}
            {% for message in messages %}
                <div class="px-2 py-1 {% if message.tags == 'success' %}bg-green-200 text-green-700{% endif %}">{{message}}</div>
            {% endfor %}
        {% endif %}
        <form method='POST'>
            {% csrf_token %}
            {{ form }}
            <button class='bg-purple-500 px-2 py-1 rounded text-white mt-3' type="submit">Update Profile</button>
            <a href="{% url 'reset-password' %}">Forget Password?</a>
        </form>
    </div>
{% endblock content %}
```
- **Detailed Explanation** ✅  
  - **`EditProfileForm`**:  
    - `Meta`: Updates `User` fields (`email`, `first_name`, `last_name`).  
    - `bio` and `profile_image`: Extra fields for `UserProfile`. `widget=forms.Textarea` makes `bio` a multiline input.  
    - `__init__`: Sets initial values from `userprofile` (passed via `kwargs`).  
    - `save`: Updates both `User` and `UserProfile`. `commit=False` delays saving until both are ready.  
  - **`EditProfileView`**:  
    - `model = User`: Targets the `User` model.  
    - `form_class`: Uses our custom form.  
    - `get_object`: Returns the current user (`self.request.user`), so no URL parameter is needed.  
    - `get_form_kwargs`: Passes the user’s `UserProfile` to the form.  
    - `get_context_data`: Ensures the form in the template has the current user and profile data.  
    - `form_valid`: Saves the form and redirects to the profile page.  
  - **Template**: Displays the form with messages and a styled submit button.  
  - **Issue**: This code assumes `self.userprofile` exists in the form, but it’s not defined yet, causing an error.

---

## **17.4 🔧 Fixing the 'userprofile' Attribute Error**

### **The Error**
- `EditProfileForm` expects `self.userprofile`, but it’s not set until `kwargs` are processed, leading to `'EditProfileForm' object has no attribute 'userprofile'`.

### **Fixed Form**
#### **forms.py**
```python
class EditProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    bio = forms.CharField(required=False, widget=forms.Textarea, label='Bio')
    profile_image = forms.ImageField(required=False, label='Profile Image')

    def __init__(self, *args, **kwargs):
        self.userprofile = kwargs.pop('userprofile', None)  # Extract userprofile
        super().__init__(*args, **kwargs)
        if self.userprofile:
            self.fields['bio'].initial = self.userprofile.bio
            self.fields['profile_image'].initial = self.userprofile.profile_image

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.userprofile:
            self.userprofile.bio = self.cleaned_data.get('bio')
            self.userprofile.profile_image = self.cleaned_data.get('profile_image')
            if commit:
                self.userprofile.save()
        if commit:
            user.save()
        return user
```
#### **Updated Profile View**
```python
class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['bio'] = user.userprofile.bio  # Access UserProfile fields
        context['profile_image'] = user.userprofile.profile_image
        context['date_joined'] = user.date_joined
        context['last_login'] = user.last_login
        return context
```
#### **Updated Template**
```html
{% extends "base.html" %}
{% block content %}
    <div class='mx-auto w-1/2 my-9'>
        {% if messages %}
            {% for message in messages %}
                <div class="px-2 py-1 {% if message.tags == 'success' %}bg-green-500{% endif %}">{{message}}</div>
            {% endfor %}
        {% endif %}
        <form method='POST' enctype='multipart/form-data'>
            {% csrf_token %}
            {{ form }}
            <button class='bg-purple-500 px-2 py-1 rounded text-white mt-3' type="submit">Update Profile</button>
        </form>
    </div>
{% endblock content %}
```
- **Detailed Explanation** ✅  
  - **Fix in `forms.py`**:  
    - `self.userprofile = kwargs.pop('userprofile', None)`: Removes `userprofile` from `kwargs` before calling `super().__init__`, avoiding the error. `None` is the default if not provided.  
    - Rest of the form uses `self.userprofile` safely.  
  - **Profile View**: Adds `bio` and `profile_image` to the context, accessed via `user.userprofile`.  
  - **Template**: Adds `enctype='multipart/form-data'` to handle file uploads (required for `profile_image`).  
  - **Result**: The form now loads and saves correctly, showing current profile data.

---

## **17.5 🔄 Customize User Model and Fix Relations**

### **Approach 2: Custom User Model**
- Instead of a separate `UserProfile`, we’ll extend the `User` model directly.

#### **models.py**
```python
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images', blank=True)
```
#### **settings.py**
```python
AUTH_USER_MODEL = 'users.CustomUser'  # Register custom user model
```
#### **forms.py**
```python
class EditProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'bio', 'profile_image']
```
#### **views.py**
```python
from django.views.generic.edit import UpdateView
from .models import CustomUser
from .forms import EditProfileForm

class EditProfileView(UpdateView):
    model = CustomUser
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save(commit=True)
        return redirect('profile')
```
#### **Update Relations**
```python
# In tasks/models.py
from django.conf import settings

class Task(models.Model):
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tasks')
```
#### **Generic User Import**
```python
from django.contrib.auth import get_user_model

User = get_user_model()  # Use CustomUser dynamically
```
- **Detailed Explanation** ✅  
  - **`CustomUser`**: Inherits from `AbstractUser`, adding `bio` and `profile_image`.  
  - **`AUTH_USER_MODEL`**: Tells Django to use `CustomUser` instead of `User`. Must be set before migrations.  
  - **Form and View**: Updated to use `CustomUser`. No separate `UserProfile` needed.  
  - **Relations**: `settings.AUTH_USER_MODEL` ensures `Task.assigned_to` uses `CustomUser`.  
  - **`get_user_model()`**: Dynamically imports the active user model, making code portable.  
  - **Migration**: Delete old migrations and database, then run `makemigrations` and `migrate`.

---

## **17.6 🎛️ Admin Panel Customization**

### **Why Customize?**
- The default admin for `CustomUser` lacks organization and doesn’t display new fields nicely.

#### **admin.py**
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'bio', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'bio', 'profile_image'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-username',)
```
- **Detailed Explanation** ✅  
  - **`@admin.register(CustomUser)`**: Registers `CustomUser` with the admin.  
  - **`class CustomUserAdmin(UserAdmin)`**: Inherits from `UserAdmin` to reuse its functionality (e.g., password hashing).  
  - **`fieldsets`**: Organizes the edit page into sections:  
    - `None`: Basic fields (`username`, `password`).  
    - `'Personal Info'`: Includes custom fields (`bio`, `profile_image`).  
    - `'Permissions'`: Controls access rights.  
    - `'Important Dates'`: Shows timestamps.  
  - **`add_fieldsets`**: Defines fields for the “Add User” page. `classes=('wide',)` makes the form wider. Includes `bio` and `profile_image`.  
  - **`list_display`**: Columns shown in the user list (e.g., `/admin/users/customuser/`).  
  - **`search_fields`**: Enables searching by these fields.  
  - **`ordering`**: Sorts users by username (descending).  
  - **Additional Info** 🌟:  
    - **Image Display**: To show `profile_image` thumbnails in the list, add a method:  
      ```python
      def profile_image_thumbnail(self, obj):
          if obj.profile_image:
              return format_html('<img src="{}" width="50" height="50" />', obj.profile_image.url)
          return "No Image"
      profile_image_thumbnail.short_description = 'Profile Image'
      list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'profile_image_thumbnail')
      ```
    - **Filters**: Add `list_filter = ('is_staff', 'is_active')` to filter users by status.  
    - **Readonly Fields**: Make `last_login` and `date_joined` readonly with `readonly_fields = ('last_login', 'date_joined')`.  
    - **Result**: A polished admin interface with custom fields, better organization, and enhanced usability.

---

# **✅ Final Summary**

1. **Create User Profile**: Added `UserProfile` with a one-to-one link to `User`.  
2. **Fix Error**: Scripted profile creation for existing users.  
3. **Edit Profile**: Used `UpdateView` and a form to edit both models.  
4. **Fix Attribute Error**: Adjusted form initialization.  
5. **Custom User Model**: Replaced `UserProfile` with `CustomUser`.  
6. **Admin Customization**: Enhanced the admin panel for `CustomUser`.  

This module provides two robust ways to customize user profiles, ensuring flexibility and a great admin experience! 🌟