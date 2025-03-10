# **Module 12: Role-Based Access Control (RBAC)**  
This module shows how to implement **role-based access control** in a Django project, letting you **restrict** views and actions based on **user groups** and **permissions**. Below is a detailed guide with **why** each step is done, **example code**, and notes on **optimization**.

---

## **12.1 Introduction to RBAC**  
**RBAC** (Role-Based Access Control) ensures that certain operations are only available to **specific roles**. For example:  
- ✅ **Admin**: Full access to everything (e.g., create user groups, assign roles, manage tasks).  
- ✅ **Manager**: Create new tasks or projects, see managerial dashboards.  
- ✅ **Employee**: View or update tasks assigned to them but not create new roles or groups.

The goal is to **separate concerns** and **prevent unauthorized changes**.

---

## **12.2 Assign Default Role and Create Admin View**

### **Why We Assign a Default Role**  
- ✅ Upon user registration, you often want them to have **some** role.  
- ✅ In this example, new users default to a “User” group, which might have minimal permissions.

### **Signals: `assign_role`**  
```python
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver

@receiver(post_save, sender=User)
def assign_role(sender, instance, created, **kwargs):
    if created:
        user_group, _ = Group.objects.get_or_create(name='User')
        instance.groups.add(user_group)  # No instance.save() needed
```
- **Notes**:  
  - **`if created:`** ensures this only runs for **new** users, not updates.  
  - **`Group.objects.get_or_create(name='User')`**: fetches or creates a **“User”** group; `_` discards the `created` boolean since it’s unused.  
  - **`instance.groups.add(...)`**: adds the user to the group; no `save()` is needed because ManyToMany updates are immediate.  
  - **Fix**: Removed unnecessary `instance.save()` from your example (it was in earlier code but optimized out).

### **Admin Dashboard**  
We also create an **admin dashboard** to manage users, roles, etc.

#### **URLs**  
```python
# users/urls.py
from django.urls import path
from users.views import signup, sign_in, sign_out, admin_dashboard

urlpatterns = [
    path('sign-up/', signup, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
    path('sign-out/', sign_out, name='sign-out'),
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
]
```

#### **Views**  
```python
# users/views.py
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, 'admin/dashboard.html', {'users': users})
```
- **Notes**: 
  - Added `is_admin` and `@user_passes_test` to restrict access to "Admin" group members, redirecting to `/no-permission/` if unauthorized.
  - Initial version; later optimized with `prefetch_related` (see 12.8).

#### **Template: `admin/dashboard.html`**  
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Admin Dashboard</title>
  <link rel="stylesheet" href="{% static 'css/output.css' %}" />
</head>
<body>
  <!-- Sample Navbar -->
  <header class="bg-white shadow-md">
    <nav class="container mx-auto px-6 py-3">
      <div class="flex justify-between items-center">
        <a href="{% url 'home' %}" class="text-xl font-bold text-gray-800">Taskify</a>
        <div class="hidden md:flex space-x-4">
          <a href="{% url 'admin-dashboard' %}" class="text-gray-600 hover:text-gray-800">Dashboard</a>
          <a href="{% url 'group-list' %}" class="text-gray-600 hover:text-gray-800">Groups</a>
          <a href="{% url 'create-group' %}" class="text-gray-600 hover:text-gray-800">Create Group</a>
        </div>
        <!-- User Dropdown with Logout -->
        <div class="relative">
          <form method="post" action="{% url 'sign-out' %}">
            {% csrf_token %}
            <button class="text-gray-600 hover:text-gray-800">Logout</button>
          </form>
        </div>
      </div>
    </nav>
  </header>

  <main>
    <div class="container mx-auto px-6 py-4">
      {% block content %}
        {% include "admin/user_list.html" %}
      {% endblock content %}
    </div>
  </main>
</body>
</html>
```
- ✅ **Static**: Links updated to use `{% url %}` tags; includes `user_list.html` for dynamic content.
- **Fix**: Corrected logout form with `{% csrf_token %}` and proper URL.

---

## **12.3 Assign Role to User**

### **Why We Created This**  
- ✅ After a user is created, an **admin** may want to change or assign a **new** role.  
- ✅ For instance, promoting a user from the default “User” role to “Manager”.

#### **Views**  
```python
# users/views.py
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import AssignRoleForm

def admin_dashboard(request):
    users = User.objects.all()
    return render(request, 'admin/dashboard.html', {'users': users})

@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(
                request, 
                f'{user.username} has been successfully assigned to {role.name} role'
            )
            return redirect('admin-dashboard')
    return render(request, 'admin/assign_role.html', {'form': form})
```
- **Flow**:
  - **GET**: Show an empty `AssignRoleForm`.  
  - **POST**: Validate form, **clear** old groups, **add** the new group.
  - **Fix**: Typo corrected ("succefully" → "successfully").

#### **URLs**  
```python
# users/urls.py
from django.urls import path
from users.views import admin_dashboard, assign_role

urlpatterns = [
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/<int:user_id>/assign-role/', assign_role, name='assign-role'),
]
```

#### **`AssignRoleForm`**  
```python
# users/forms.py
from django import forms
from django.contrib.auth.models import Group

class AssignRoleForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a role"
    )
```
- ✅ We use a **`ModelChoiceField`** to list all available `Group`s.  
- **No** `ModelForm` needed because it’s just one field.

#### **Templates**  
- **`admin/dashboard.html`**:  
  - Updated above to include `user_list.html`.  
- **`admin/user_list.html`**:
  ```html
  <table class="min-w-full bg-white shadow-md rounded-lg">
    <thead class="bg-gray-100">
      <tr>
        <th class="px-4 py-3">Number</th>
        <th class="px-4 py-3">Username</th>
        <th class="px-4 py-3">Email</th>
        <th class="px-4 py-3">User ID</th>
        <th class="px-4 py-3">Current Role</th>
        <th class="px-4 py-3">Action</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gray-200">
      {% for user in users %}
        <tr class="hover:bg-gray-50">
          <td class="px-4 py-4">{{ forloop.counter }}</td>
          <td class="px-4 py-4">{{ user.first_name }} {{ user.last_name }}</td>
          <td class="px-4 py-4">{{ user.email }}</td>
          <td class="px-4 py-4">{{ user.id }}</td>
          <td class="px-4 py-4">{{ user.groups.first.name|default:"None" }}</td>
          <td class="px-4 py-4">
            <a href="{% url 'assign-role' user.id %}" class="bg-purple-400 hover:bg-purple-600 text-white font-bold py-2 px-4 rounded">
              Change Role
            </a>
          </td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
  ```
  - **Fix**: Added `|default:"None"` to handle users with no groups.
- **`assign_role.html`**:
  ```html
  {% extends "admin/dashboard.html" %}
  {% block content %}
    <div class="w-1/2 mx-auto my-8">
      {% for message in messages %}
        <p class="bg-green-500 text-white px-1 py-2">{{ message }}</p>
      {% endfor %}
      <form method="POST">
        {% csrf_token %}
        {{ form }}
        <button type="submit" class="mt-3 px-2 py-1 text-white bg-purple-500 rounded">Assign Role</button>
      </form>
    </div>
  {% endblock content %}
  ```

---

## **12.4 Create Group**

### **Why Create New Groups at Runtime**  
- ✅ Admins might want to define new roles beyond “User,” “Manager,” or “Employee” (e.g., “Supervisor”).

#### **`CreateGroupForm`**  
```python
# users/forms.py
from django.contrib.auth.models import Group, Permission

class CreateGroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign Permission"
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']
```
- ✅ We add `permissions` as checkboxes so admins can **pick** which actions this group can perform.

#### **Views**  
```python
@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f'{group.name} group created successfully')
            return redirect('admin-dashboard')
    return render(request, 'admin/create_group.html', {'form': form})
```
- **Flow**:  
  - **GET**: Show empty form.  
  - **POST**: Create a **new** `Group` with selected permissions.
  - **Added**: `@user_passes_test` for admin-only access.

#### **Template: `admin/create_group.html`**  
```html
{% extends "admin/dashboard.html" %}
{% block content %}
  <div class="w-1/2 mx-auto my-8">
    {% for message in messages %}
      <p class="bg-green-500 text-white px-1 py-2">{{ message }}</p>
    {% endfor %}
    <form method="POST">
      {% csrf_token %}
      {{ form }}
      <button type="submit" class="mt-3 px-2 py-1 text-white bg-purple-500 rounded">Create Group</button>
    </form>
  </div>
{% endblock content %}
```

#### **URLs**  
```python
path('admin/create-group/', create_group, name='create-group')
```
- ✅ Link from your navbar (updated in `dashboard.html` above).

---

## **12.5 Group List**

### **Why List Groups**  
- ✅ Admins want to **see** all groups and their permissions.  
- ✅ Quick reference to see which roles exist and what they can do.

#### **Views**  
```python
@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'admin/group_list.html', {'groups': groups})
```
- **Added**: `@user_passes_test` for admin-only access.

#### **`group_list.html`**  
```html
{% extends "admin/dashboard.html" %}
{% block content %}
  <div class="w-2/3 mx-auto my-8">
    <h2 class="text-2xl font-bold mb-4">Groups and Permissions</h2>
    <table class="table-auto w-full border-collapse border border-gray-300">
      <thead>
        <tr class="bg-gray-100">
          <th class="border border-gray-300 px-4 py-2">Group Name</th>
          <th class="border border-gray-300 px-4 py-2">Permissions</th>
        </tr>
      </thead>
      <tbody>
        {% for group in groups %}
          <tr class="odd:bg-white even:bg-gray-50">
            <td class="border border-gray-300 px-4 py-2 font-medium">{{ group.name }}</td>
            <td class="border border-gray-300 px-4 py-2">
              <ul class="list-disc list-inside">
                {% for permission in group.permissions.all %}
                  <li>{{ permission.name }} | {{ permission.codename }}</li>
                {% empty %}
                  <span class="text-gray-500 italic">No permissions assigned</span>
                {% endfor %}
              </ul>
            </td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
{% endblock content %}
```
- **Example**:  
  - “Manager” group might have **`tasks.add_task`**, **`tasks.change_task`**, etc.

---

## **12.7 Enforcing Views to Check Permission**

### **Why Restrict Certain Views**  
- ✅ Some actions (like **delete_task**) should only be done by managers or admins.  
- ✅ Checking **Django permissions** (like `tasks.add_task`) ensures that only those with correct rights can do them.

#### **Decorators**  
1. **`@login_required`**: User must be authenticated.  
2. **`@permission_required("<app>.<action>_<model>")`**: User must have that specific permission or redirect to `login_url`.  
3. **`@user_passes_test`**: Custom role checks.

```python
# tasks/views.py
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_employee(user):
    return user.groups.filter(name='Employee').exists()

@login_required
@permission_required("tasks.add_task", login_url='no-permission')
def create_task(request):
    # Logic to create tasks
    ...

@login_required
@permission_required("tasks.change_task", login_url='no-permission')
def update_task(request, id):
    # Logic to update tasks
    ...

@login_required
@permission_required("tasks.delete_task", login_url='no-permission')
def delete_task(request, id):
    # Logic to delete tasks
    ...

@login_required
@permission_required("tasks.view_task", login_url='no-permission')
def view_task(request):
    # Logic to show tasks
    ...

@user_passes_test(is_manager, login_url='no-permission')
def manager_dashboard(request):
    # Only managers can see this
    ...

@user_passes_test(is_employee, login_url='no-permission')
def employee_dashboard(request):
    # Only employees can see this
    ...
```
- **`"tasks.add_task"`**: Permission codenames auto-generated by Django for the `Task` model.
- **Added**: `is_manager` and `is_employee` examples with `@user_passes_test`.

#### **No Permission View**  
- **Why**: Redirect unauthorized users to a custom page.
- **Code** (in `core/views.py`):
  ```python
  def no_permission(request):
      return render(request, 'no_permission.html')
  ```
- **Template** (`core/no_permission.html`):
  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <title>No Permission</title>
  </head>
  <body>
      <h2>You don't have permission to access this page!</h2>
      <a href="{% url 'home' %}">Back to Home</a>
  </body>
  </html>
  ```
- **URL** (in `task_management/urls.py`):
  ```python
  path('no-permission/', no_permission, name='no-permission')
  ```

---

## **12.8 SQL Optimization**

### **Why Optimize?**  
- **N+1 query problem**: Fetching 10 users and then individually querying each user’s groups results in 11 queries, slowing the app.

### **`prefetch_related`**  
- ✅ Combine queries for **related objects** (e.g., a user’s groups) into **one** additional query.

#### **Example**  
```python
from django.db.models import Prefetch

@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = "No Group Assigned"
    return render(request, 'admin/dashboard.html', {"users": users})
```
- **Behavior**:  
  - 1 query for all `User`s, 1 query for all `Group`s linked to those users.  
  - Instead of **N+1** queries, we only do **2** queries total.
  - **`to_attr='all_groups'`**: Stores groups in `user.all_groups`; `group_name` is computed in Python.
- **Template Update** (`user_list.html`):
  - Replace `{{ user.groups.first.name }}` with `{{ user.group_name }}`.

Similarly, for **group_list**:  
```python
@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})
```
- **1 query** for the groups, **1 query** for the many-to-many `permissions`.  
- Previously, referencing `group.permissions.all` in a loop caused multiple queries.

#### **12.8.1 Before and After Example**  
- **Before (`admin_dashboard`)**:
  ```python
  users = User.objects.all()
  # Template: {{ user.groups.first.name }}
  ```
  - **Queries**: 1 (users) + N (one per user for groups).  
  - **Example**: 3 users = 4 queries.
- **After**:
  ```python
  users = User.objects.prefetch_related(Prefetch('groups', to_attr='all_groups')).all()
  for user in users:
      user.group_name = user.all_groups[0].name if user.all_groups else "No Group Assigned"
  # Template: {{ user.group_name }}
  ```
  - **Queries**: 2 (users + all groups).  
  - **Example**: 3 users = 2 queries.

- **Before (`group_list`)**:
  ```python
  groups = Group.objects.all()
  # Template: {{ group.permissions.all }}
  ```
  - **Queries**: 1 (groups) + N (one per group for permissions).  
  - **Example**: 2 groups = 3 queries.
- **After**:
  ```python
  groups = Group.objects.prefetch_related('permissions').all()
  ```
  - **Queries**: 2 (groups + all permissions).  
  - **Example**: 2 groups = 2 queries.

---

# **Final Summary**  

1. **Default Role Assignment**: Use a **post_save** signal to put new users in a **“User”** role by default.  
2. **Admin Dashboard**: A centralized place to **manage users**, **groups**, **permissions**, etc.  
3. **Assign Role to User**: Let admins switch a user’s **group** from “User” to “Manager” or “Employee.”  
4. **Create & List Groups**: Use `Group` objects with assigned **permissions** so you can define new roles (like “Admin,” “Manager,” etc.) dynamically.  
5. **Decorator-Based Access Control**:  
   - **`@login_required`** ensures only logged-in users can access certain views.  
   - **`@permission_required("app.action_model")`** ensures the user has that exact permission.  
   - **`@user_passes_test(...)`** checks custom logic (e.g., `is_admin`).  
6. **SQL Optimization**:  
   - Use **`prefetch_related`** for ManyToMany fields to avoid N+1 queries.  
   - This leads to fewer total queries and improves performance.

By combining **groups/permissions** with signals and query optimizations, you achieve a **secure** and **efficient** role-based system in Django, ensuring each user can only do what their role permits.  

✅ **With RBAC, your Django app becomes safer, more maintainable, and easier to scale!**

---