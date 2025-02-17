# **Module 8: Django CRUD Operations**

Below is a **detailed** note-format explanation of how to create a **dynamic dashboard** and implement **CRUD (Create, Read, Update, Delete)** in Django.  
We’ll weave in **emojis** (✅, ❌, 🌟, etc.) and **explicit references** to highlight important points.

---

## **8.1 🌟 Dynamic Dashboard**

### **Why Dynamic?**  
- **Static data** is ❌ outdated in real-time.  
- **Dynamic data** is ✅ automatically updated to reflect changes in your database.

### **1. Setting Up the Manager Dashboard**

#### **Views: `manager_dashboard`**
```python
from django.shortcuts import render
from django.db.models import Q, Count
from tasks.models import Task

def manager_dashboard(request):
    # ✅ 1) Fetch all tasks
    tasks = Task.objects.all()

    # ✅ 2) Calculate stats
    total_task = tasks.count()
    completed_task = Task.objects.filter(status='COMPLETED').count()
    in_progress_task = Task.objects.filter(status='IN_PROGRESS').count()
    pending_task = Task.objects.filter(status='PENDING').count()

    # ✅ 3) Send data to template
    context = {
        "tasks": tasks,
        "total_task": total_task,
        "completed_task": completed_task,
        "in_progress_task": in_progress_task,
        "pending_task": pending_task
    }
    return render(request, "dashboard/manager_dashboard.html", context=context)
```
- **Explanation**  
  - We use **`Task.objects.all()`** to retrieve all tasks.  
  - We filter tasks by **`status`** to show how many have each status.  
  - **`context`** passes these numbers to the template.

#### **Template: `dashboard.html`**
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title><b>{% block title %}{% endblock title %}</b></title>
  <script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>
  <link rel="stylesheet" href="{% static "css/output.css" %}">
</head>

<body class="bg-gray-50 p-6">
  <div class="mx-auto max-w-[1400px]">
    <!-- Header -->
    <header class="flex items-center justify-between mb-8">
      <h1 class="text-2xl font-semibold">Dashboard</h1>
      <div class="flex items-center gap-4">
        <button class="relative rounded-full p-2 hover:bg-gray-100">
          <!-- Notification Icon -->
        </button>
        <button class="h-10 w-10 rounded-full bg-blue-500 font-semibold text-white">
          B
        </button>
      </div>
    </header>

    <main>
      <!-- Stats Grid -->
      <div class="grid grid-cols-4 gap-6">
        <!-- Total Task -->
        <div class="bg-white rounded-xl p-6 shadow-sm">
          <h3 class="text-sm font-medium text-gray-500 mb-4">Total Task</h3>
          <div class="flex justify-between items-start">
            <div>
              <p class="text-3xl font-semibold mb-1">{{ total_task }}</p>
              <p class="text-gray-500 text-sm">111 Last Month</p>
            </div>
            <div class="bg-blue-100 p-3 rounded-full">
              <!-- Some Icon -->
            </div>
          </div>
        </div>
        <!-- Completed Task -->
        <div class="bg-white rounded-xl p-6 shadow-sm">
          <h3 class="text-sm font-medium text-gray-500 mb-4">Completed Task</h3>
          <div class="flex justify-between items-start">
            <div>
              <p class="text-3xl font-semibold mb-1">{{ completed_task }}</p>
              <p class="text-gray-500 text-sm">111 Last Month</p>
            </div>
            <div class="bg-green-100 p-3 rounded-full">
              <!-- Some Icon -->
            </div>
          </div>
        </div>
        <!-- Task in Progress -->
        <div class="bg-white rounded-xl p-6 shadow-sm">
          <h3 class="text-sm font-medium text-gray-500 mb-4">Task in Progress</h3>
          <div class="flex justify-between items-start">
            <div>
              <p class="text-3xl font-semibold mb-1">{{ in_progress_task }}</p>
              <p class="text-gray-500 text-sm">111 Last Month</p>
            </div>
            <div class="bg-yellow-100 p-3 rounded-full">
              <!-- Some Icon -->
            </div>
          </div>
        </div>
        <!-- Pending -->
        <div class="bg-white rounded-xl p-6 shadow-sm">
          <h3 class="text-sm font-medium text-gray-500 mb-4">Todos</h3>
          <div class="flex justify-between items-start">
            <div>
              <p class="text-3xl font-semibold mb-1">{{ pending_task }}</p>
              <p class="text-gray-500 text-sm">111 Last Month</p>
            </div>
            <div class="bg-purple-100 p-3 rounded-full">
              <!-- Some Icon -->
            </div>
          </div>
        </div>
      </div>

      {% block tasks %}{% endblock tasks %}
    </main>
  </div>
  {% include "footer.html" %}
</body>
</html>
```
- **Explanation**  
  - We display **4 stats**: total tasks, completed, in-progress, pending.  
  - **`{{ total_task }}`, `{{ completed_task }}`, etc.** are from the **context**.

#### **Template: `manager_dashboard.html`**  
```html
{% extends "dashboard/dashboard.html" %}
{% block title %}Manager Dashboard{% endblock title %}
{% block tasks %}
<div class="bg-white rounded-xl shadow-sm">
  <!-- Table Header -->
  <div class="grid grid-cols-4 items-center p-4 mt-8 text-gray-500 text-sm border-b border-gray-100">
    <p>TASK TITLE</p>
    <p>PRIORITY</p>
    <p>TEAM</p>
    <p>CREATED AT</p>
  </div>

  {% for task in tasks %}
  <div class="grid grid-cols-4 items-center p-4 gap-4 text-gray-500 text-sm border-b border-gray-100">
    <!-- Task Title -->
    <div class="flex items-center gap-2">
      <div class="w-2 h-2 bg-green-500 rounded-full"></div>
      <div>{{ task.title }}</div>
    </div>

    <!-- Priority (OneToOne Relationship) -->
    <div>
      <span class="px-3 py-1 text-sm bg-blue-200 rounded-2xl text-blue-500">
        {{ task.details.get_priority_display }}
      </span>
    </div>

    <!-- Team (ManyToMany Relationship) -->
    <div>
      <div class="flex -space-x-2">
        {% for emp in task.assigned_to.all %}
        <div class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm border-2 border-white">
          {{ emp.name|slice:":2" }}
        </div>
        {% endfor %}
      </div>
    </div>

    <!-- Created At (time since) -->
    <div class="text-gray-500 text-sm">
      {{ task.created_at|timesince }} ago
    </div>
  </div>
  {% endfor %}
</div>
{% endblock tasks %}
```
- **Note**  
  - We access **reverse relation** for priority with `task.details.priority`.  
  - We use **`get_priority_display`** to show human-readable text (✅ **High**, ❌ `H`).  
  - We slice employee names to **first 2 letters** with `|slice:":2"`.

---

## **8.2 🚀 Optimizing Database Queries**  

### **Why Optimize?**  
- Too many queries = ❌ slow performance.  
- Using `select_related` and `prefetch_related` = ✅ fewer queries.

#### **Using `select_related`**  
- ✅ Great for **OneToOneField** or **ForeignKey**.  
- Performs a **JOIN** at the **database level**.

#### **Using `prefetch_related`**  
- ✅ Great for **ManyToMany** or **Reverse ForeignKey**.  
- Performs **separate queries** and links objects in **Python memory**.

### **1. Example of Combined Optimization**  
```python
def manager_dashboard(request):
    tasks = Task.objects.select_related('details').prefetch_related('assigned_to').all()
    
    # Using aggregations for quick counts
    counts = Task.objects.aggregate(
        total_task=Count('id'),
        completed_task=Count('id', filter=Q(status='COMPLETED')),
        in_progress_task=Count('id', filter=Q(status='IN_PROGRESS')),
        pending_task=Count('id', filter=Q(status='PENDING'))
    )

    context = {
        "tasks": tasks,
        "counts": counts
    }
    return render(request, "dashboard/manager_dashboard.html", context)
```
- **Explanation**  
  - **`select_related('details')`**: pulls **TaskDetail** in **one** query.  
  - **`prefetch_related('assigned_to')`**: optimizes **ManyToMany** for employees.  
  - **`aggregate(...)`**: calculates stats in **1 query** rather than multiple.

#### **Updating the Template**  
Use **`counts.total_task`**, **`counts.completed_task`**, etc.:
```html
<p class="text-3xl font-semibold mb-1">{{ counts.total_task }}</p>
```

---

## **8.3 🔗 Dynamic Query with URL Parameters**

### **Why Do We Need This?**  
- **Filtering** tasks by status (e.g., “Completed”) via **click** on the dashboard.  

#### **1. Views: Handling `type` GET Parameter**  
```python
def manager_dashboard(request):
    # Get "type" from URL, default to "all"
    type = request.GET.get('type', 'all')
    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')

    # ✅ Filter tasks by "type"
    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type == 'in_progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status='PENDING')
    else:
        tasks = base_query.all()

    # Aggregations
    counts = Task.objects.aggregate(
        total_task=Count('id'),
        completed_task=Count('id', filter=Q(status='COMPLETED')),
        in_progress_task=Count('id', filter=Q(status='IN_PROGRESS')),
        pending_task=Count('id', filter=Q(status='PENDING'))
    )

    return render(request, "dashboard/manager_dashboard.html", {
        "tasks": tasks,
        "counts": counts
    })
```

#### **2. Template: Anchor Tags**  
```html
<!-- Completed Task Card -->
<a href="{% url 'manager_dashboard' %}?type=completed">
  <div class="bg-white rounded-xl p-6 shadow-sm">
    <h3>Completed Task</h3>
    <p class="text-3xl font-semibold">{{ counts.completed_task }}</p>
  </div>
</a>
```

#### **3. `urls.py` with Named Routes**  
```python
urlpatterns = [
    path('dashboard/', manager_dashboard, name="manager_dashboard"),
]
```
- **Check** ✅: We rely on **`name="manager_dashboard"`** in templates.  
- **Advantage** ✅: If we change `'dashboard/'` to something else, we only update **`urls.py`**, not every link.

---

## **8.4 📝 Create Multiple Objects in a Single View**

### **Scenario**  
- A **Task** has **details** in `TaskDetail`.  
- We want to **create both** simultaneously in the **same** form submission.  

#### **1. `TaskDetailModelForm`**  
```python
# forms.py
from django import forms
from tasks.models import Task, TaskDetail

class TaskDetailModelForm(forms.ModelForm):
    class Meta:
        model = TaskDetail
        fields = ['priority', 'notes']
```

#### **2. Views: `create_task`**  
```python
def create_task(request):
    task_form = TaskModelForm()
    taskdetail_form = TaskDetailModelForm()

    if request.method == "POST":
        task_form = TaskModelForm(request.POST)
        taskdetail_form = TaskDetailModelForm(request.POST)
        if task_form.is_valid() and taskdetail_form.is_valid():
            # ✅ 1) Create Task
            task = task_form.save()
            
            # ✅ 2) Create TaskDetail (commit=False)
            taskdetail = taskdetail_form.save(commit=False)
            taskdetail.task = task
            taskdetail.save()

            messages.success(request, "Task Created Successfully")
            return redirect('create_task')  # Or any other route

    context = {
        "task_form": task_form,
        "taskdetail_form": taskdetail_form
    }
    return render(request, 'task_form.html', context)
```
- **Explanation**  
  - **`commit=False`**: we create `TaskDetail` object **first** but don’t save.  
  - We assign **`taskdetail.task = task`** so that the **foreign key** is linked.  
  - Then we **save** the details.  

#### **3. Template: `task_form.html`**  
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Task Form</title>
  <link rel="stylesheet" href="{% static "css/output.css" %}">
</head>
<body>
  <div class="w-1/2 mx-auto mt-8">
    <!-- ✅ Display Django Messages -->
    {% if messages %}
      {% for message in messages %}
        <div class="px-2 py-1 
          {% if message.tags == 'success' %}bg-green-500{% endif %}
          {% if message.tags == 'error' %}bg-red-500{% endif %}
        ">
          {{ message }}
        </div>
      {% endfor %}
    {% endif %}

    <!-- ✅ Form -->
    <form action="" method="POST">
      {% csrf_token %}
      {{ task_form.as_p }}
      {{ taskdetail_form.as_p }}
      <button class="bg-rose-600 px-3 py-2 text-white mt-2 rounded-md" type="submit">Submit</button>
    </form>
  </div>
</body>
</html>
```
- **Check** ✅: We display both the **`task_form`** and **`taskdetail_form`** fields.

---

## **8.5 ✏️ Update Existing Task**

### **Why Similar to Create?**  
- **Update** follows the same form approach, except we provide an **instance** of the object we want to modify.

#### **1. `urls.py`**  
```python
urlpatterns = [
    ...
    path('update_task/<int:id>/', update_task, name='update_task'),
]
```

#### **2. Views: `update_task`**  
```python
def update_task(request, id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task)

    # ✅ Check if task has details
    if task.details:
        taskdetail_form = TaskDetailModelForm(instance=task.details)
    else:
        taskdetail_form = TaskDetailModelForm()

    if request.method == "POST":
        task_form = TaskModelForm(request.POST, instance=task)
        taskdetail_form = TaskDetailModelForm(request.POST, instance=task.details)
        if task_form.is_valid() and taskdetail_form.is_valid():
            updated_task = task_form.save()
            updated_detail = taskdetail_form.save(commit=False)
            updated_detail.task = updated_task
            updated_detail.save()

            messages.success(request, "Task Updated Successfully")
            return redirect('update_task', id=id)

    context = {
        "task_form": task_form,
        "taskdetail_form": taskdetail_form
    }
    return render(request, 'task_form.html', context)
```
- **Notes**  
  - **`instance=task`** pre-fills the form with existing data.  
  - If the **task doesn’t have details** (maybe new?), we create a blank detail form.  

#### **3. `manager_dashboard.html` - Adding Edit Button**  
```html
<div class="flex items-center gap-2">
  <div class="w-2 h-2 bg-green-500 rounded-full flex-shrink-0"></div>
  <span class="flex-grow">{{ task.title }}</span>
  <a href="{% url 'update_task' task.id %}" class="px-2 py-1 bg-green-500 text-white">Edit</a>
</div>
```
- **Check** ✅: We pass `task.id` to the **update** URL, so we know which task to edit.

---

## **8.6 🗑️ Delete Task from Database**  

### **1. `urls.py`**  
```python
urlpatterns = [
    ...
    path('delete_task/<int:id>/', delete_task, name='delete_task'),
]
```

### **2. Views: `delete_task`**  
```python
def delete_task(request, id):
    if request.method == "POST":
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, "Task Deleted Successfully")
        return redirect('manager_dashboard')
    
    messages.error(request, "Something went wrong")
    return redirect('manager_dashboard')
```
- **Check** ✅: Must use **POST** to confirm the action.  
- **Cross** ❌: GET method shouldn’t generally be used for destructive actions.

### **3. Template: Delete Button**  
```html
<form action="{% url 'delete_task' task.id %}" method="POST">
  {% csrf_token %}
  <button class="px-2 py-1 bg-red-500 text-white" type="submit">Delete</button>
</form>
```
- **Check** ✅: We add the **CSRF token** to protect from malicious requests.  
- **Check** ✅: Displays a red “Delete” button next to each task.

### **4. Showing Success or Error Messages**  
```html
<div>
  {% if messages %}
    {% for message in messages %}
      <div class="px-2 py-1
        {% if message.tags == 'success' %}bg-green-500{% endif %}
        {% if message.tags == 'error' %}bg-red-500{% endif %}
      ">
        {{ message }}
      </div>
    {% endfor %}
  {% endif %}
</div>
```
- **Check** ✅: Placed in a common template (e.g., `dashboard.html`) so that the **message** is visible everywhere.

---

# **✅ Final Summary and Code Organization**

1. **`manager_dashboard(request)`**  
   - Shows **READ** (list of tasks) and basic stats.  
   - Uses **optimized queries** (`select_related`, `prefetch_related`, `aggregate`).

2. **`create_task(request)`**  
   - Creates both **Task** and **TaskDetail** in **one** request.  
   - Uses **two ModelForms**.

3. **`update_task(request, id)`**  
   - Similar approach to **create**, but uses **`instance=task`** and **`instance=task.details`** for pre-filled data.

4. **`delete_task(request, id)`**  
   - **POST** method to delete a specific task.  
   - Uses **`messages`** to display success/failure.

5. **Templates**  
   - **`dashboard.html`** (parent)  
   - **`manager_dashboard.html`** (child) for listing tasks.  
   - **`task_form.html`** for create/update forms.

6. **`urls.py`**  
   - Named routes: **`manager_dashboard`**, **`create_task`**, **`update_task`**, **`delete_task`**.  
   - Use **`{% url ... %}`** in templates to link to them.

✅ **This holistic approach** covers everything from **optimizing queries** with **`select_related`** and **`prefetch_related`** to building a **CRUD** interface with **Django forms** and **Django messages**.  