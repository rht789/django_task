# **Module 10: Building Django Authentication**  

---

## **10.1 Introduction to the Django Admin Panel**  

### **What is the Admin Panel?**  
- The Django admin panel is a **powerful tool** offering a **user-friendly interface** for managing your application’s **models**, **database records**, **users**, **permissions**, and more.  
- By default, you can access it at:  
  ```
  http://127.0.0.1:8000/admin/
  ```

### **Why Use the Admin Panel?**  
- ✅ **Fast & Convenient CRUD** on database tables without writing raw SQL.  
- ✅ **Built-in** features for searching, filtering, and managing data.  
- ❌ Without admin, you’d have to build your own entire backend system for data management.

### **Registering Models in `admin.py`**  
To make models appear in the admin panel, **register** them:
```python
# tasks/admin.py

from django.contrib import admin
from tasks.models import Task, TaskDetail, Employee, Project

admin.site.register(Task)
admin.site.register(TaskDetail)
admin.site.register(Employee)
admin.site.register(Project)
```
- After this, you can see and **modify** these models in `/admin/`.

---

## **10.2 Signup Using `UserCreationForm`**  

### **Project URL Structure**  
In the **root** `urls.py`, you typically include **`users/urls.py`** so you don’t have to define all **user routes** in the main file:
```python
# task_management/urls.py

from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from tasks.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home),
    path("tasks/", include("tasks.urls")),
    path("users/", include("users.urls")),  # ✅ include the users app
] + debug_toolbar_urls()
```
- ✅ This approach keeps your project organized by **app**.

### **Users App URLs**  
```python
# users/urls.py

from django.urls import path
from users.views import signup

urlpatterns = [
    path('sign-up/', signup, name='sign-up'),
]
```
- ✅ A simple route for **sign-up** is set here.

### **Views Using Django’s Built-in `UserCreationForm`**  
```python
# users/views.py

from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)  # For debugging
            form.save()  # ✅ Creates a new user in the database
    return render(request, "registration/signup.html", {"form": form})
```
- ✅ **`UserCreationForm`** includes `username`, `password1`, and `password2`.
- ❌ Doesn’t provide additional fields (like email) by default.

### **Template: `signup.html`**  
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Sign Up</title>
</head>
<body>
  <p>Hi</p>
  <div>
    <form action="" method="POST">
      {% csrf_token %}
      {{ form.as_p }}
      <button type="submit">Sign Up</button>
    </form>
  </div>
</body>
</html>
```
- ✅ It shows a basic sign-up form with **username**, **password1**, **password2**.

---

## **10.3 Customizing `UserCreationForm`**  

### **Why Customize?**  
- The default `UserCreationForm` only has **username & password fields**.
- If you need **additional fields** like `email`, `first_name`, `last_name`, you can extend it.

### **Creating a `RegisterForm`**  
```python
# users/forms.py

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email']
    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None  # Remove default help text
```
- ✅ Extends `UserCreationForm` to add or remove fields as needed.

### **Updating Your View to Use `RegisterForm`**  
```python
# users/views.py

from users.forms import RegisterForm

def signup(request):
    if request.method == 'GET':
        form = RegisterForm()
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print("Form is not valid")
    return render(request, 'registration/register.html', {'form': form})
```
- ✅ Now the sign-up process includes **email**, **first_name**, **last_name**.

---

## **10.4 Form Field Validation**  

### **Why Might We Need Custom Validation?**  
- We want to **enforce** certain password rules (minimum length, uppercase, digits, special characters) or other constraints.

### **Building a `CustomRegisterForm`** (without `UserCreationForm`)  
```python
# users/forms.py

from django import forms
from django.contrib.auth.models import User

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
```
- ✅ **`clean_<fieldname>`** is automatically called for validation of that field.
- ✅ `self.cleaned_data` holds valid data if no `ValidationError` is raised.

---

## **10.5 Field and Non-Field Errors**  

### **Field-Level vs. Non-Field-Level**  
- **Field-level errors**: Checking **one field** on its own (e.g., password length).  
- **Non-field errors**: Checking **interdependency** of **multiple fields** (e.g., matching password1 & password2).

### **Adding Non-Field Validation**  
```python
def clean(self):
    cleaned_data = super().clean()
    password1 = cleaned_data.get('password1')
    password2 = cleaned_data.get('password2')

    if password1 and password2 and password1 != password2:
        raise forms.ValidationError("Passwords do not match.")

    return cleaned_data
```
- ✅ This ensures the two passwords match.

### **Handling Email or Username Uniqueness**  
```python
def clean_email(self):
    email = self.cleaned_data.get('email')
    email_exist = User.objects.filter(email=email).exists()
    if email_exist:
        raise forms.ValidationError("This email is already associated with an account.")
    return email

def clean_username(self):
    username = self.cleaned_data.get('username')
    username_exist = User.objects.filter(username=username).exists()
    if username_exist:
        raise forms.ValidationError("Username already exists.")
    return username
```
- ✅ Check the database for duplicates.  
- ❌ If it exists, raise an error.

### **Final `CustomRegisterForm`** Example  
```python
class CustomRegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','password2','email']

    # Field-level validations (username, email, password1, etc.)
    # ...
    
    def clean(self):
        cleaned_data = super().clean()
        pwd1 = cleaned_data.get('password1')
        pwd2 = cleaned_data.get('password2')
        if pwd1 and pwd2 and pwd1 != pwd2:
            raise forms.ValidationError("Password Do Not Match")
        return cleaned_data
```

### **Using the Form in `views.py`**  
```python
def signup(request):
    if request.method == 'GET':
        form = CustomRegisterForm()
    else:  # POST
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # ❌ Don’t save yet
            user.set_password(form.cleaned_data['password1'])  # ✅ Hash password
            user.save()
        else:
            print("Form is not valid")

    return render(request, 'registration/register.html', {'form': form})
```
- **`set_password(...)`** ensures the password is hashed for **secure** storage in the database.

### **Template Example**  
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Register</title>
</head>
<body>
  {% if form.non_field_errors %}
    {% for error in form.non_field_errors %}
      <p>{{ error }}</p>
    {% endfor %}
  {% endif %}

  <form action="" method="POST">
    {% csrf_token %}
    {% for field in form %}
      <p>
        {{ field.label }}: {{ field }}
        {% if field.errors %}
          <ul>
            {% for e in field.errors %}
              <li>{{ e }}</li>
            {% endfor %}
          </ul>
        {% endif %}
      </p>
    {% endfor %}
    <button type="submit">Sign Up</button>
  </form>
</body>
</html>
```
- ✅ We handle **non-field errors** for the password mismatch.  

---

## **10.6 Login with a Custom HTML Form**  

### **Why a Custom Form?**  
- Django includes **built-in login** (via `django.contrib.auth.views.LoginView`).  
- ✅ A custom form gives you **full control** over design and logic.

### **Views: `sign_in`**  
```python
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def sign_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)  # ✅ Checks DB credentials

        if user is not None:
            # ✅ credentials valid
            login(request, user)
            return redirect('home')
        else:
            # ❌ credentials invalid
            return render(request, 'registration/signin.html', {'error': 'Invalid Username or Password'})
    
    return render(request, "registration/signin.html")
```
- **`authenticate(...)`**: Returns a **User** object if valid, else **None**.
- **`login(request, user)`**: Logs the user in, storing session info.

### **URLs: `sign_in`**  
```python
# users/urls.py
from django.urls import path
from users.views import sign_in

urlpatterns = [
    path('sign-in/', sign_in, name='sign-in'),
]
```

### **Template: `signin.html`**  
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Sign In</title>
</head>
<body>
  {% if error %}
    <p style="color:red;">{{ error }}</p>
  {% endif %}
  
  <form method="POST">
    {% csrf_token %}
    <label>Username</label>
    <input type="text" name="username" required>
    
    <label>Password</label>
    <input type="password" name="password" required>
    
    <button type="submit">Sign In</button>
  </form>
</body>
</html>
```
- **If** authentication fails, we display **“Invalid Username or Password”**.

### **A Simple `home` Page**  
```python
# core/views.py

from django.shortcuts import render

def home(request):
    return render(request,'home.html')
```
```python
# home.html
<!DOCTYPE html>
<html>
<head><title>Home</title></head>
<body>
  <p>Welcome to the home page</p>
  {% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}</p>
  {% else %}
    <p>Anonymous User</p>
  {% endif %}
</body>
</html>
```
- ✅ `request.user` becomes the **logged-in** user once `login()` is called.

---

## **10.7 Logout**  

### **Why?**  
- **Logging out** ends the user’s session. 
- **No** longer recognized as an authenticated user.

### **Flow**  
1. User clicks a **sign-out** button or form.  
2. A **POST** request is sent to your logout route.  
3. Django logs the user out.  
4. User is **redirected** to sign-in or any chosen page.

### **Views: `sign_out`**  
```python
from django.contrib.auth import logout

def sign_out(request):
    if request.method == 'POST':
        logout(request)  # ✅ kills the session
        return redirect('sign-in')
    return redirect('sign-in')
```
- ❌ Using GET for logout is discouraged (less secure).  
- ✅ Using POST ensures an explicit user action to log out.

### **URLs**  
```python
# users/urls.py
from django.urls import path
from users.views import sign_out

urlpatterns = [
    path('sign-out/', sign_out, name='sign-out'),
    ...
]
```

### **Template Example** (`home.html` or similar)  
```html
{% if user.is_authenticated %}
  <p>Welcome, {{ user }}</p>
  <form action="{% url 'sign-out' %}" method="POST">
    {% csrf_token %}
    <button type="submit">Sign Out</button>
  </form>
{% else %}
  <p>Anonymous user</p>
{% endif %}
```
- **On** POST submission, the user is logged out and then **redirected**.

#### **Detailed Flow**  
1. **Sign Out Form** → POST request to `/users/sign-out/`.  
2. **`sign_out`** view calls `logout(request)`, sets user to an **anonymous session**.  
3. **Redirects** to `sign-in`.  
4. On next GET, the user sees the **sign-in** page.

---

# **Summary: Building Django Authentication**  
1. **Admin Panel** (`/admin/`) – Quickly manage your app’s data by registering models in `admin.py`.  
2. **Signup**:
   - **Built-in** `UserCreationForm` for basic username/password.  
   - **Custom** forms to add extra fields or advanced validations (email, name, etc.).  
3. **Field Validation**:
   - **`clean_<field>()`** for field-specific checks.  
   - **`clean()`** for cross-field logic (e.g., password confirm).
4. **Login**:
   - Use **`authenticate`** + **`login`** to verify credentials and set a user session.  
   - Provide a **custom HTML** form for better UX.
5. **Logout**:
   - Use **`logout`** in a POST route to safely end the session.  
   - Redirect to **sign-in** (or home).
6. **`request.user`** & **`is_authenticated`**:
   - **`request.user`** is the user object once logged in.  
   - **`user.is_authenticated`** is ✅ if the user is logged in, ❌ otherwise.

With these **detailed** steps, you have a **complete** approach to **building authentication** in Django—including **admin usage**, **signup**, **login**, **logout**, and **custom validations** for a polished, secure system.