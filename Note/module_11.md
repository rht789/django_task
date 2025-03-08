# **Module 11: Django Signals**

Here’s an **expanded**, **organized**, and **emoji-rich** summary of how to use **Django Signals**, **email sending**, **environment variables**, and **authentication forms**. Each subsection clarifies **why** certain decisions were made and **how** they improve the application’s flexibility.

---

## **11.1 Introduction to Signals**
Django **signals** let different parts of your application **communicate** without direct references (i.e., “decoupling”). They allow you to **trigger actions** whenever certain events occur (e.g., model saving, deleting, or user authentication events).

### **Why Use Signals?**
- ✅ **Automation**: Automatically perform extra logic (e.g., sending emails, cleaning data) when a specific **event** happens.  
- ✅ **Loose Coupling**: Different features can react to events without referencing each other’s code.  
- ❌ Without signals, you might scatter logic around multiple places or forget key steps (like emailing assigned employees).

### **Common Django Model Signals**
1. **`pre_save`**  
   - **When**: Just **before** an object is saved (`instance.save()`).  
   - **Example Use Case**: Force or sanitize certain fields (e.g., set `is_completed = True` automatically).  
   ```python
   from django.db.models.signals import pre_save
   from django.dispatch import receiver
   from tasks.models import Task

   @receiver(pre_save, sender=Task)
   def notify_task_creation(sender, instance, **kwargs):
       print("sender:", sender)
       print("instance:", instance)
       instance.is_completed = True  # Example logic
   ```

2. **`post_save`**  
   - **When**: Right **after** an object is saved.  
   - **Extra Argument**: `created` indicates if it’s a **new** instance (True) or an **update** (False).  
   - **Example Use Case**: Set additional fields, send a confirmation email, or create linked data after a new record is created.  
   ```python
   from django.db.models.signals import post_save
   from django.dispatch import receiver

   @receiver(post_save, sender=Task)
   def notify_task_after_save(sender, instance, created, **kwargs):
       if created:
           instance.is_completed = True
           instance.save()
   ```

3. **`pre_delete`**  
   - **When**: **Before** an object is deleted from the database.  
   - **Example Use Case**: Clean up related data or confirm if deletion is allowed.

4. **`post_delete`**  
   - **When**: **After** an object is deleted.  
   - **Example Use Case**: Perform final cleanup—like clearing logs, sending a removal notification, etc.

5. **`pre_init`**  
   - **When**: **Before** a model’s `__init__()` method is called.  
   - **Rarely Used** but can be handy for advanced initialization.

6. **`post_init`**  
   - **When**: **After** a model’s `__init__()` method is called.  
   - **Example Use Case**: Set up instance-specific data right after creation, but before any saving.

7. **`m2m_changed`**  
   - **When**: A ManyToManyField changes (e.g., adding or removing items).  
   - **Example Use Case**: Notify employees when they’re assigned/unassigned from a Task.  

### **Signal Registration**
- ✅ Signals must be **registered** in `apps.py` to work:
  ```python
  # users/apps.py
  from django.apps import AppConfig

  class UsersConfig(AppConfig):
      name = 'users'
      def ready(self):
          import users.signals
  ```
  ```python
  # users/__init__.py
  default_app_config = 'users.apps.UsersConfig'
  ```

---

## **11.2 m2m Implementation in Task Management**
In our **task management** system, we have a **ManyToMany** relationship between **Task** and **Employee** (e.g., `Task.assigned_to`). To **automate email notifications** whenever employees are assigned, we use the **`m2m_changed`** signal.

### **Why We Added This**
- ✅ We want **automatic emails** each time a new employee is assigned to a task.  
- ✅ This ensures that all involved employees are immediately informed without manually sending emails.

### **Example Email Configuration**
```python
# settings.py (partial)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "example@gmail.com"
EMAIL_HOST_PASSWORD = "password-or-app-password"
```
- **Note**: Using **Gmail’s SMTP** requires correct ports and TLS settings.

### **Using `m2m_changed`**
```python
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Task

@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_employees_on_task_creation(sender, instance, action, **kwargs):
    if action == 'post_add':
        assigned_emails = [emp.email for emp in instance.assigned_to.all()]
        send_mail(
            "New Task Assigned",
            f"You have been assigned to the task: {instance.title}",
            "example@gmail.com",
            assigned_emails,
            fail_silently=False,
        )
```
- **Key Points**:  
  - ✅ `sender = Task.assigned_to.through` references the **“through” table** (the M2M link).  
  - **`action='post_add'`** means employees were **just added**. We can then gather their emails and notify them.

---

## **11.3 Post Delete**
We also want to **manually delete** related data if we set `on_delete=DO_NOTHING` on certain relationships. This is because “DO_NOTHING” means Django won’t automatically remove related objects.

### **Why We Added This**
- ✅ We changed `TaskDetail` to `on_delete=models.DO_NOTHING` because we **didn’t** want automatic deletion.  
- ✅ However, we **do** want to remove details manually to ensure **custom** cleanup logic.

### **Example with `post_delete`**
```python
from django.db.models.signals import post_delete
from django.dispatch import receiver
from tasks.models import Task

@receiver(post_delete, sender=Task)
def delete_associated_details(sender, instance, **kwargs):
    if instance.details:
        instance.details.delete()
        print("Task detail also deleted")
```
- **Behavior**:  
  - **After** a `Task` is deleted, if it has a `TaskDetail`, we manually delete that detail to keep the database consistent.

---

## **11.4 Setting an Environmental Variable**
We often need **environment variables** to store **sensitive** or **configuration** data (like **DB credentials**, **API keys**, or **secret keys**) outside our codebase.

### **Why We Use Environment Variables**
- ✅ **Security**: Keep secrets out of source control.  
- ✅ **Flexibility**: Change environment details (e.g., database or email settings) without editing code.

### **Steps to Set Up**

1. **Install `python-decouple`**  
   ```bash
   pip install python-decouple
   ```

2. **Create a `.env` File**
   ```plaintext
   SECRET_KEY=django-insecure-$rd=2...
   DB_NAME=task_management
   DB_USER=postgres
   DB_PASSWORD=1234
   DB_HOST=localhost
   DB_PORT=5432

   EMAIL_HOST=smtp.gmail.com
   EMAIL_USE_TLS=True
   EMAIL_PORT=587
   EMAIL_HOST_USER=example@gmail.com
   EMAIL_HOST_PASSWORD=some-app-password

   FRONTEND_URL=http://127.0.0.1:8000/
   ```
   - ✅ **Never** commit this `.env` file (add it to `.gitignore`).

3. **Reference `.env` in `settings.py`**
   ```python
   from decouple import config

   SECRET_KEY = config("SECRET_KEY")
   DEBUG = True

   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': config('DB_NAME'),
           'USER': config('DB_USER'),
           'PASSWORD': config('DB_PASSWORD'),
           'HOST': config('DB_HOST'),
           'PORT': config('DB_PORT', cast=int)
       }
   }

   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = config('EMAIL_HOST')
   EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
   EMAIL_PORT = config('EMAIL_PORT', cast=int)
   EMAIL_HOST_USER = config('EMAIL_HOST_USER')
   EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

   FRONTEND_URL = config('FRONTEND_URL')
   ```
   - **Explanation**: We read secrets from `.env` to keep them out of our code.

---

## **11.5 Sending User Activation Email**
Sometimes we want **newly registered** users to **verify** their email. One approach is to **disable** (`is_active=False`) them by default and **email** an activation link.

### **Why We Added This**
- ✅ We ensure only **real** email addresses can activate accounts.  
- ✅ Useful for security and to reduce spam or fake accounts.

### **Implementation with `post_save`**
```python
# users/signals.py
@receiver(post_save, sender=User)
def send_activation_mail(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}"
        subject = "Activate Your Account"
        message = (
            f"Hi {instance.username},\n\n"
            f"Please click this link to activate your account:\n\n"
            f"{activation_url}\n\n"
            f"Thank you."
        )
        recipient = [instance.email]

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient,
            fail_silently=False
        )
```
- **Check**: We only do this if `created == True`, i.e., **new** user.

### **Views: Marking User as Inactive**
```python
def signup(request):
    ...
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password1'))
        user.is_active = False  # ❌ not active until email link clicked
        user.save()
        messages.success(request, "A confirmation mail sent...")
    ...
```
- **Once** the user clicks the link, you’d have another view to **activate** them.

---

## **11.6 Login with Django’s `AuthenticationForm`**
Django’s `AuthenticationForm` is a built-in form that **validates** username/password using the **Django auth system**.

### **Why We Use `AuthenticationForm`**
- ✅ Less code: No need to define your own username/password fields.  
- ✅ Built-in security checks (e.g., verifying hashed passwords).

### **In `forms.py`**
```python
from django.contrib.auth.forms import AuthenticationForm
from tasks.forms import StyledFormMixin

class LoginForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    # ✅ Inherits fields from AuthenticationForm
    # ✅ StyledFormMixin for consistent design
```
### **Views**
```python
def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login success")
            return redirect('home')
    return render(request, "registration/signin.html", {'form': form})
```
### **Template**
```html
<form method="POST">
  {% csrf_token %}
  {{ form }}
  <button type="submit">Sign In</button>
</form>
```
- **When** the user provides correct credentials, `login(request, user)` logs them in.

---

# **Final Summary**

1. **Signals**:  
   - **`pre_save` & `post_save`** – React to model saves (e.g., auto-setting fields, emailing on creation).  
   - **`pre_delete` & `post_delete`** – Handle tasks before or after deletion (cleanup, notifications).  
   - **`m2m_changed`** – Respond to changes in ManyToMany fields (like assigning employees).

2. **Manual Cleanup**: If you **override** default `on_delete` behavior (e.g., using `DO_NOTHING`), you can still do **cleanup** with signals like `post_delete`.

3. **Environment Variables**:  
   - Keep secrets in `.env`, read them with `decouple.config()`.  
   - Improves **security** and **maintainability**.

4. **User Activation Flow**:  
   - **`post_save`** on `User` can email a link with a **token**.  
   - Mark the user as **`is_active=False`** until they click the link.

5. **Django’s AuthenticationForm**:  
   - Replaces manual login checks, offers a clean `form.is_valid()` approach.  
   - Use `login(request, form.get_user())` to authenticate in one step.

By combining **signals**, **environment variables**, **email notifications**, and **authentication forms**, you build a **secure**, **scalable**, and **maintainable** Django application.  

✅ **Enjoy the power of Django’s flexible architecture with signals, environment-based configuration, and out-of-the-box authentication!**



