# **Module 16: Django Auth Views & Custom Filters**

This module explores Django’s built-in **authentication views** (auth views) as Class-Based Views (CBVs) and how to customize them for login, logout, password management, and more. We’ll also cover creating **custom template filters** to enhance template rendering. Let’s dive in with detailed examples and explanations!

---

## **16.1 🌟 Intro to Auth Views and LoginView**

### **What Are Auth Views?**
- Django provides pre-built CBVs in `django.contrib.auth.views` for common authentication tasks like login, logout, and password resets.  
- These save time by handling the heavy lifting (e.g., form validation, user authentication) while allowing customization.

### **LoginView Basics**
- `LoginView` is a CBV for user login. By default, it uses a template at `registration/login.html`, but we can override this.

#### **urls.py**
```python
from django.contrib.auth.views import LoginView
from django.urls import path

urlpatterns = [
    path('sign-in/', LoginView.as_view(template_name='registration/signin.html'), name='sign-in'),
]
```
#### **settings.py**
```python
LOGIN_URL = '/users/sign-in/'  # Where unauthenticated users are redirected
LOGIN_REDIRECT_URL = '/tasks/dashboard/'  # Where users go after login
```
- **Detailed Explanation** ✅  
  - **`LoginView.as_view(template_name='registration/signin.html')`**: Uses Django’s `LoginView` directly without a custom class. We override the default template (`registration/login.html`) to `registration/signin.html`, matching our project’s naming. `.as_view()` turns the CBV into a callable view for the URL.  
  - **`path('sign-in/', ...)`**: Maps `/sign-in/` to the login page. The `name='sign-in'` lets us reference it in templates or redirects (e.g., `{% url 'sign-in' %}`).  
  - **`settings.py`**:  
    - `LOGIN_URL`: Defines the login page path. If a user tries to access a protected page (e.g., via `LoginRequiredMixin`), they’re sent here. Must be a full path, not just the name.  
    - `LOGIN_REDIRECT_URL`: After login, users are sent to `/tasks/dashboard/`. This is the success URL unless overridden.

---

## **16.2 🚀 Customizing LoginView**

### **Why Customize?**
- The default `LoginView` is functional but plain. We want to use our own form and handle post-login redirection dynamically (e.g., to a page the user tried to access).

#### **Original FBV**
```python
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import LoginForm

def sign_in(request):
    form = LoginForm()  # Empty form for GET
    if request.method == "POST":
        form = LoginForm(data=request.POST)  # Bind form with POST data
        if form.is_valid():  # Check if credentials are valid
            user = form.get_user()  # Get the authenticated user
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to home
    return render(request, "registration/signin.html", {'form': form})  # Render form
```

#### **Custom CBV**
```python
from django.contrib.auth.views import LoginView
from .forms import LoginForm

class CustomLoginView(LoginView):
    form_class = LoginForm  # Custom form
    template_name = 'registration/signin.html'  # Custom template

    def get_success_url(self):  # Override redirect behavior
        next_url = self.request.GET.get('next')  # Check for 'next' parameter
        return next_url if next_url else super().get_success_url()  # Use next or default
```
#### **urls.py**
```python
from .views import CustomLoginView

urlpatterns = [
    path('sign-in/', CustomLoginView.as_view(), name='sign-in'),
]
```
- **Detailed Explanation** ✅  
  - **`class CustomLoginView(LoginView)`**: Inherits from `LoginView` to customize it.  
  - **`form_class = LoginForm`**: Uses our custom `LoginForm` (assumed to be defined in `forms.py`) instead of Django’s default `AuthenticationForm`. This might add styling or extra fields.  
  - **`template_name = 'registration/signin.html'`**: Specifies our template, matching the FBV.  
  - **`def get_success_url(self)`**: Overrides the default redirect (set in `LOGIN_REDIRECT_URL`).  
    - `self.request.GET.get('next')`: Checks the URL for a `next` parameter (e.g., `/sign-in/?next=/dashboard/`). This appears when a user tries to access a protected page and is redirected to login.  
    - `return next_url if next_url else super().get_success_url()`: If `next` exists, redirects there (e.g., `/dashboard/`); otherwise, falls back to `LOGIN_REDIRECT_URL` (`/tasks/dashboard/`).  
  - **Why This Matters**: Without this, after login, users always go to the default redirect, ignoring the page they originally wanted. This fix improves user experience.  
  - **`urls.py`**: Maps `/sign-in/` to our custom view. No need to pass `template_name` here since it’s in the class.

---

## **16.3 👤 ProfileView Using TemplateView**

### **What Is TemplateView?**
- `TemplateView` is a CBV for rendering a static template without forms or model queries. It’s perfect for simple pages like a user profile.

#### **Template: `accounts/profile.html`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>User Profile</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">
    <div class="flex min-h-screen">
        <!-- Sidebar -->
        <aside class="w-64 bg-white shadow-md">
            <div class="p-4">
                <h2 class="text-xl font-semibold text-gray-800">Menu</h2>
            </div>
            <nav class="mt-6">
                <a href="#" class="block py-2 px-4 text-gray-700 bg-gray-200 hover:bg-gray-300">Profile</a>
                <a href="#" class="block py-2 px-4 text-gray-700 hover:bg-gray-200">Edit Profile</a>
                <a href="#" class="block py-2 px-4 text-gray-700 hover:bg-gray-200">Change Password</a>
            </nav>
        </aside>
        <!-- Main Content -->
        <main class="flex-1 p-8">
            <h1 class="text-3xl font-bold text-gray-800 mb-8">User Profile</h1>
            <div class="bg-white shadow-md rounded-lg p-6">
                <div class="flex items-center mb-6">
                    <img src="https://png.pngtree.com/png-clipart/20231019/original/pngtree-user-profile-avatar-png-image_13369988.png" 
                         alt="User Avatar" class="w-24 h-24 rounded-full object-cover mr-6" />
                    <div>
                        <h2 class="text-2xl font-semibold text-gray-800">{{ name }}</h2>
                        <p class="text-gray-600">Software Developer</p>
                    </div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <h3 class="text-lg font-semibold text-gray-700 mb-2">Personal Information</h3>
                        <p class="text-gray-600"><span class="font-medium">Email:</span> {{ email }}</p>
                        <p class="text-gray-600"><span class="font-medium">Username:</span> {{ username }}</p>
                        <p class="text-gray-600"><span class="font-medium">Location:</span> New York, USA</p>
                    </div>
                    <div>
                        <h3 class="text-lg font-semibold text-gray-700 mb-2">Account Information</h3>
                        <p class="text-gray-600"><span class="font-medium">Member Since:</span> {{ date_joined }}</p>
                        <p class="text-gray-600"><span class="font-medium">Last Login:</span> {{ last_login }}</p>
                    </div>
                </div>
                <div class="mt-6">
                    <h3 class="text-lg font-semibold text-gray-700 mb-2">Bio</h3>
                    <p class="text-gray-600">
                        Passionate software developer with 5 years of experience in web technologies...
                    </p>
                </div>
            </div>
        </main>
    </div>
</body>
</html>
```
#### **views.py**
```python
from django.views.generic import TemplateView

class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'  # Template to render
    
    def get_context_data(self, **kwargs):  # Add user data to context
        context = super().get_context_data(**kwargs)
        user = self.request.user  # Current logged-in user
        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()  # Full name or empty string
        context['date_joined'] = user.date_joined
        context['last_login'] = user.last_login
        return context
```
#### **urls.py**
```python
from .views import ProfileView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
]
```
- **Detailed Explanation** ✅  
  - **`class ProfileView(TemplateView)`**: Inherits from `TemplateView`, which simply renders a template with optional context. No forms or models are needed here.  
  - **`template_name = 'accounts/profile.html'`**: Specifies the template to display.  
  - **`def get_context_data(self, **kwargs)`**: Adds data to the template:  
    - `super().get_context_data(**kwargs)`: Gets any default context from `TemplateView`.  
    - `self.request.user`: Accesses the current logged-in user (requires authentication middleware).  
    - Adds `username`, `email`, `name` (from `get_full_name()`), `date_joined`, and `last_login` to the context, which the template uses (e.g., `{{ email }}`).  
  - **Template**: Uses Tailwind CSS for styling. Displays user info in a sidebar and main content layout. Static fields like “Location” and “Bio” are hardcoded, while others are dynamic.  
  - **`urls.py`**: Maps `/profile/` to this view. Visiting this URL shows the user’s profile.

---

## **16.4 ✂️ Custom Template Filter**

### **Why Custom Filters?**
- Django’s default date filters (e.g., `{{ date_joined|date:"Y-m-d" }}`) are rigid. A custom filter can format dates more naturally (e.g., “Today at 3:45 PM”).

#### **Setup: `users/templatetags/custom_filters.py`**
```python
from django import template
from datetime import datetime
from django.utils import timezone

register = template.Library()  # Create a filter registry

@register.filter  # Register the filter
def humanized_date(value):  # Function to format dates
    if value:  # Check if date exists
        today = datetime.now().date()  # Current date
        value = timezone.localtime(value)  # Convert to local timezone
        if value.date() == today:  # Same day
            return f"Today at {value.strftime('%I:%M %p')}"  # e.g., "Today at 3:45 PM"
        if value.date() == today.replace(day=today.day - 1):  # Yesterday
            return f"Yesterday at {value.strftime('%I:%M %p')}"
        else:  # Older dates
            return f"{value.date().strftime('%B %d')}, {value.strftime('%I:%M %p')}"  # e.g., "March 19, 11:00 AM"
    return "No login record available"  # Fallback for None
```
#### **Updated Template Snippet**
```html
{% load custom_filters %}  <!-- Load the filter -->
<p class="text-gray-600">
    <span class="font-medium">Member Since:</span> {{ date_joined|humanized_date }}
</p>
<p class="text-gray-600">
    <span class="font-medium">Last Login:</span> {{ last_login|humanized_date }}
</p>
```
- **Detailed Explanation** ✅  
  - **Setup**:  
    - Create `users/templatetags/` folder (in the `users` app) with `__init__.py` (empty) and `custom_filters.py`.  
    - `register = template.Library()`: Initializes a registry for custom filters.  
  - **`@register.filter`**: Marks `humanized_date` as a template filter.  
  - **`def humanized_date(value)`**: Takes a datetime value (e.g., `user.last_login`):  
    - `if value`: Ensures the value isn’t `None` (e.g., if the user never logged in).  
    - `today = datetime.now().date()`: Gets today’s date for comparison.  
    - `value = timezone.localtime(value)`: Converts the UTC-stored datetime to the local timezone (set in `settings.py`).  
    - **Conditions**:  
      - `value.date() == today`: If the date matches today, formats as “Today at [time]” (12-hour with AM/PM).  
      - `today.replace(day=today.day - 1)`: Calculates yesterday’s date. If it matches, formats as “Yesterday at [time]”.  
      - Else: Formats as “Month Day, Time” (e.g., “March 19, 11:00 AM”).  
    - `return "No login record available"`: Fallback for `None` values.  
  - **Template**:  
    - `{% load custom_filters %}`: Loads the filter file (after restarting the server and registering `users` in `INSTALLED_APPS`).  
    - `{{ last_login|humanized_date }}`: Applies the filter to `last_login`, displaying it human-readably.

---

## **16.5 🚪 LogoutView**

### **What Is LogoutView?**
- `LogoutView` logs the user out and redirects them. It’s simple and often used directly in URLs.

#### **urls.py**
```python
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('sign-out/', LogoutView.as_view(), name='sign-out'),
]
```
#### **settings.py**
```python
LOGOUT_REDIRECT_URL = '/'  # Redirect to homepage after logout
```
- **Detailed Explanation** ✅  
  - **`LogoutView.as_view()`**: Uses Django’s built-in `LogoutView` to end the user’s session. No custom view is needed here.  
  - **`path('sign-out/', ...)`**: Maps `/sign-out/` to logout.  
  - **`LOGOUT_REDIRECT_URL`**: After logout, sends the user to `/`. Without this, it defaults to a basic logout page (if a template is provided).  
  - **How It Works**: Clears the session and redirects. No template is required unless you override it.

---

## **16.6 🔑 PasswordChangeView**

### **Why Customize?**
- `PasswordChangeView` changes a user’s password, but we want it styled with our form.

#### **forms.py**
```python
from django.contrib.auth.forms import PasswordChangeForm
from .mixins import StyledFormMixin  # Assumed mixin for styling

class CustomPasswordChangeForm(StyledFormMixin, PasswordChangeForm):
    pass  # Inherits styling from mixin
```
#### **views.py**
```python
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

class ChangePassword(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/password_change.html'

class PasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'
```
#### **urls.py**
```python
from .views import ChangePassword, PasswordChangeDoneView

urlpatterns = [
    path('password-change/', ChangePassword.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
]
```
#### **Templates**
- **`accounts/password_change.html`**
```html
{% extends "base.html" %}
{% block content %}
    <div class='mx-auto w-1/2 my-9'>
        {% if messages %}
            {% for message in messages %}
                <div class="px-2 py-1 {% if message.tags == 'success' %}bg-green-200 text-green-700{% endif %}">{{ message }}</div>
            {% endfor %}
        {% endif %}
        <form method='POST'>
            {% csrf_token %}
            {{ form }}
            <button class='bg-purple-500 px-2 py-1 rounded text-white mt-3' type="submit">Change Password</button>
        </form>
    </div>
{% endblock content %}
```
- **`accounts/password_change_done.html`**
```html
<p>Please go back to <a href="{% url 'dashboard' %}">Dashboard</a></p>
```
- **Detailed Explanation** ✅  
  - **`forms.py`**: `CustomPasswordChangeForm` inherits from `PasswordChangeForm` and a `StyledFormMixin` (assumed to add CSS classes).  
  - **`ChangePassword`**:  
    - `form_class`: Uses our styled form.  
    - `template_name`: Renders the form page.  
  - **`PasswordChangeDoneView`**: Shows a success page after the password is changed.  
  - **Templates**:  
    - `password_change.html`: Displays the form with messages (e.g., success or errors). `{% csrf_token %}` adds security.  
    - `password_change_done.html`: Simple confirmation with a dashboard link.  
  - **`urls.py`**: Maps `/password-change/` to the form and `/password-change/done/` to the success page.

---

## **16.7 📧 PasswordResetView**

### **What Is PasswordResetView?**
- Sends a password reset email to the user.

#### **forms.py**
```python
from django.contrib.auth.forms import PasswordResetForm
from .mixins import StyledFormMixin

class CustomPasswordResetForm(StyledFormMixin, PasswordResetForm):
    pass
```
#### **views.py**
```python
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib import messages

class PasswordReset(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')

    def get_context_data(self, **kwargs):  # Add email context
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context

    def form_valid(self, form):  # Add success message
        messages.success(self.request, 'A reset email has been sent. Please check your email.')
        return super().form_valid(form)
```
#### **urls.py**
```python
from .views import PasswordReset

urlpatterns = [
    path('password_reset/', PasswordReset.as_view(), name='reset-password'),
]
```
- **Detailed Explanation** ✅  
  - **`form_class`**: Uses a styled form for email input.  
  - **`success_url = reverse_lazy('sign-in')`**: Redirects to `/sign-in/` after success. `reverse_lazy` delays URL resolution until needed.  
  - **`get_context_data`**: Adds `protocol` (http/https) and `domain` (e.g., `localhost:8000`) to the context for the email link.  
  - **`form_valid`**: Adds a success message before sending the email and redirecting.  
  - **How It Works**: User enters their email, gets a reset link, and is redirected to login.

---

## **16.8 🔐 PasswordResetConfirmView**

### **What Is PasswordResetConfirmView?**
- Handles the reset link from the email, letting the user set a new password.

#### **forms.py**
```python
from django.contrib.auth.forms import SetPasswordForm
from .mixins import StyledFormMixin

class CustomPasswordResetConfirmForm(StyledFormMixin, SetPasswordForm):
    pass
```
#### **views.py**
```python
from django.contrib.auth.views import PasswordResetConfirmView

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')
    
    def form_valid(self, form):
        messages.success(self.request, 'Password Reset Successfully!')
        return super().form_valid(form)
```
#### **urls.py**
```python
from .views import CustomPasswordResetConfirmView

urlpatterns = [
    path('password-reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
```
- **Detailed Explanation** ✅  
  - **`form_class`**: Uses a styled form for new password input.  
  - **`template_name`**: Reuses `reset_password.html` (could be separate).  
  - **`success_url`**: Redirects to `/sign-in/` after reset.  
  - **`form_valid`**: Adds a success message.  
  - **URL**: `<uidb64>/<token>` are from the email link, verifying the reset request.

---

## **16.9 📩 Custom Email Template**

### **Why Customize?**
- Default reset emails are plain text. We want a styled HTML email.

#### **Template: `registration/reset_email.html`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 0; padding: 0; }
        .email-container { max-width: 600px; margin: 20px auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }
        .header { background-color: #4CAF50; color: #ffffff; text-align: center; padding: 20px; }
        .body { padding: 20px; }
        .footer { background-color: #f4f4f4; text-align: center; padding: 10px; font-size: 12px; color: #888888; }
        .button { display: inline-block; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>Password Reset Request</h1>
        </div>
        <div class="body">
            <p>Hi {{ user.get_full_name|default:user.username }},</p>
            <p>You recently requested to reset your password. Click below to reset it:</p>
            <p>
                <a href="{{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}" class="button">
                    Reset Password
                </a>
            </p>
            <p>If you didn’t request this, ignore this email. The link expires in 24 hours.</p>
        </div>
        <div class="footer">
            © {{ year }} Your Website. All rights reserved.<br>
            Contact us at <a href="mailto:support@taskmanager.com">support@taskmanager.com</a>.
        </div>
    </div>
</body>
</html>
```
#### **Updated View**
```python
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'registration/reset_email.html'  # Custom email template
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        context['year'] = datetime.now().year  # Add current year
        return context

    def form_valid(self, form):
        messages.success(self.request, 'A reset email has been sent. Please check your email.')
        return super().form_valid(form)
```
- **Detailed Explanation** ✅  
  - **`html_email_template_name`**: Tells `PasswordResetView` to use our HTML email template instead of plain text.  
  - **Template**:  
    - Inline CSS for email client compatibility.  
    - `{{ user.get_full_name|default:user.username }}`: Shows full name or username if no full name exists.  
    - `{{ protocol }}://{{ domain }}{% url ... %}`: Builds the reset link dynamically.  
  - **`get_context_data`**: Adds `protocol`, `domain`, and `year` to the email context.  
  - **Result**: Sends a styled email with a clickable reset button.

---

# **✅ Final Summary**

1. **LoginView**: Basic login with custom template and redirect handling.  
2. **ProfileView**: Displays user info with `TemplateView`.  
3. **Custom Filter**: Formats dates naturally (e.g., “Today at 3:45 PM”).  
4. **LogoutView**: Simple logout with redirect.  
5. **PasswordChangeView**: Styled password change with success page.  
6. **PasswordResetView**: Sends custom reset emails.  
7. **PasswordResetConfirmView**: Resets passwords via email link.  
8. **Custom Email**: Styled HTML email for resets.  

This module covers Django’s auth CBVs and custom enhancements, making authentication user-friendly and visually appealing! 🌟