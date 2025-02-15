Here's the **formatted and detailed** version of **Module 7: Django ORM** with all explanations, examples, and clarifications.

---

# **7. ORM (Object-Relational Mapping) in Django**
## **7.1 What is Django ORM?**
Django **ORM (Object-Relational Mapping)** is a tool that allows us to interact with a **relational database using Python code** instead of raw SQL.

### **Benefits of Django ORM**
1. **Reduces complexity** – No need to write complex SQL queries manually.
2. **Increases readability** – Makes database operations easier to understand.
3. **Saves time** – Fetch, insert, update, and delete data with simple Python code.

---

## **7.1.1 Django Debug Toolbar**
### **What is Django Debug Toolbar?**
Django Debug Toolbar is a **set of panels** that display **debug information** about requests, responses, and database queries in your Django web application.

### **Why Use Django Debug Toolbar?**
1. **Database Query Analysis**
   - Shows all executed **SQL queries** during a request.
   - Highlights **slow** and **duplicate queries**.
   - Helps in optimizing database interactions.

2. **Performance Monitoring**
   - Shows the execution time for **view processing, middleware execution, and template rendering**.
   - Helps identify **performance bottlenecks**.

3. **Template Debugging**
   - Displays which **templates** were used and **context variables** passed.
   - Helps in troubleshooting **data rendering issues**.

4. **Cache Inspection**
   - Shows **cache hits and misses**.
   - Helps in optimizing **caching strategies**.

5. **Request/Response Inspection**
   - Displays **HTTP headers, GET/POST parameters, cookies, and session data**.
   - Helps debug authentication and API issues.

6. **Signals and Logging**
   - Shows Django **signals triggered** during the request.
   - Integrates with **Python’s logging system**.

7. **Custom Panels**
   - Developers can create **custom panels** to monitor specific data (e.g., third-party API calls).

8. **Ease of Use**
   - Simple **installation and configuration**.
   - Provides real-time debugging information.

---

# **7.2 Reset Database in Django**
### **Steps to Reset the PostgreSQL Database**
1. **Delete the current database in PostgreSQL (using pgAdmin or CLI).**
2. **Delete all previous migration files** (except `__init__.py`) in the `migrations` folder.
3. **Create a new database in PostgreSQL (pgAdmin).**
4. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### **Updated Models After Reset**
```python
from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed')
    ]

    project = models.ForeignKey("Project", on_delete=models.CASCADE, default=1)
    assigned_to = models.ManyToManyField(Employee)
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="PENDING")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TaskDetail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_OPTIONS = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low')
    )

    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Details for Task: {self.task}"
```
✅ **Django automatically assigns a primary key (`id` field)**, but we can manually set one:
```python
task_id = models.CharField(max_length=200, primary_key=True)
```

---

# **7.3 Populating the Database Using Faker**
## **Why Use Faker?**
Manually creating **data via Django shell** is **time-consuming**. Instead, we use **Faker**, a Python package that generates **fake data**.

### **Steps to Populate Database**
1. **Install Faker**:
   ```bash
   pip install faker
   ```
2. **Create a `populate_db.py` file in the root folder** and add the following code:

```python
import os
import django
from faker import Faker
import random
from tasks.models import Employee, Project, Task, TaskDetail

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')
django.setup()

def populate_db():
    fake = Faker()

    # Create Projects
    projects = [Project.objects.create(
        name=fake.bs().capitalize(),
        description=fake.paragraph(),
        start_date=fake.date_this_year()
    ) for _ in range(5)]
    print(f"Created {len(projects)} projects.")

    # Create Employees
    employees = [Employee.objects.create(
        name=fake.name(),
        email=fake.email()
    ) for _ in range(10)]
    print(f"Created {len(employees)} employees.")

    # Create Tasks
    tasks = []
    for _ in range(20):
        task = Task.objects.create(
            project=random.choice(projects),
            title=fake.sentence(),
            description=fake.paragraph(),
            due_date=fake.date_this_year(),
            status=random.choice(['PENDING', 'IN_PROGRESS', 'COMPLETED']),
            is_completed=random.choice([True, False])
        )
        task.assigned_to.set(random.sample(employees, random.randint(1, 3)))
        tasks.append(task)
    print(f"Created {len(tasks)} tasks.")

    # Create Task Details
    for task in tasks:
        TaskDetail.objects.create(
            task=task,
            assigned_to=", ".join([emp.name for emp in task.assigned_to.all()]),
            priority=random.choice(['H', 'M', 'L']),
            notes=fake.paragraph()
        )
    print("Populated TaskDetails for all tasks.")
    print("Database populated successfully!")

populate_db()
```

✅ **To Run the Script in Django Shell**:
```bash
from populate_db import populate_db
populate_db()
```

---

# **7.4 Retrieving Data from the Database**
## **Viewing All Tasks**
In `views.py`:
```python
from django.shortcuts import render
from .models import Task

def view_task(request):
    tasks = Task.objects.all()
    return render(request, "view_task.html", {"tasks": tasks})
```

In `view_task.html`:
```html
<ul>
    {% for task in tasks %}
        <li>{{ task }}</li>
    {% endfor %}
</ul>
```

✅ **Fetching a Single Task by `id`**:
```python
task = Task.objects.get(id=1)
taskpk = Task.objects.get(pk=1)
task1 = Task.objects.first()
```
---

# **7.5 Advanced Filtering in Django ORM (Lookups)**
Django provides **lookups** to filter data based on specific conditions.

### **1. Exact Match**
- Returns tasks where `title` is exactly `"Open"` (case-sensitive).
```python
tasks = Task.objects.filter(title__exact="Open")
```

### **2. Case-Insensitive Exact Match**
- Same as `exact`, but **case-insensitive**.
```python
tasks = Task.objects.filter(title__iexact="open")
```

### **3. Contains**
- Checks if a **field contains a given value** (case-sensitive).
```python
tasks = Task.objects.filter(title__contains="O")
```

### **4. Case-Insensitive Contains**
- Same as `contains`, but **case-insensitive**.
```python
tasks = Task.objects.filter(title__icontains="o")
```

### **5. `in` Lookup**
- Checks if a **field’s value exists in a given list**.
```python
tasks = Task.objects.filter(priority__in=["HIGH", "MEDIUM"])
```

### **6. Greater Than & Less Than**
| Operator | Description | Example |
|----------|------------|---------|
| `gt` | Finds values **greater than** a value | `Task.objects.filter(due_date__gt="2025-01-01")` |
| `gte` | Finds values **greater than or equal to** a value | `Task.objects.filter(due_date__gte="2025-01-01")` |
| `lt` | Finds values **less than** a value | `Task.objects.filter(due_date__lt="2025-12-31")` |
| `lte` | Finds values **less than or equal to** a value | `Task.objects.filter(due_date__lte="2025-12-31")` |

✅ **Example in Our Project**
```python
tasks = Task.objects.filter(due_date__lte="2025-12-31", priority__in=["H", "M"])
```
This **fetches tasks due before 2025-12-31** that have **High or Medium priority**.

---

### **7. StartsWith & EndsWith**
| Lookup | Description | Example |
|--------|-------------|---------|
| `startswith` | Finds fields that **start with** a given value (case-sensitive). | `Task.objects.filter(title__startswith="A")` |
| `istartswith` | Same as `startswith`, but **case-insensitive**. | `Task.objects.filter(title__istartswith="a")` |
| `endswith` | Finds fields that **end with** a given value (case-sensitive). | `Task.objects.filter(title__endswith="Z")` |
| `iendswith` | Same as `endswith`, but **case-insensitive**. | `Task.objects.filter(title__iendswith="z")` |

---

### **8. `range()` Lookup**
- Finds values **between two numbers or dates**.
```python
tasks = Task.objects.filter(due_date__range=["2025-01-01", "2025-12-31"])
```

---

### **9. Finding NULL Values**
- Finds records where a **specific field is NULL**.
```python
tasks = Task.objects.filter(notes__isnull=True)
```

---

### **10. Checking If Data Exists**
- Returns `True` or `False` depending on whether results exist.
```python
Task.objects.filter(status="COMPLETED").exists()
```

---

### **11. Using `Q` Objects for Complex Queries**
✅ **`Q` allows combining multiple conditions using `&`, `|`, and `~`**.

| Operator | Meaning | Example |
|----------|---------|---------|
| `&` | AND | `Task.objects.filter(Q(status="PENDING") & Q(priority="H"))` |
| `|` | OR | `Task.objects.filter(Q(status="PENDING") | Q(priority="H"))` |
| `~` | NOT | `Task.objects.filter(~Q(status="PENDING"))` |

✅ **Example in Our Project**
```python
from django.db.models import Q

tasks = Task.objects.filter(
    Q(due_date__lte="2025-12-31") & (Q(priority="H") | Q(priority="M"))
)
```
- Retrieves **tasks due before 2025-12-31** that have **High or Medium priority**.

---

# **7.6 Optimizing Queries Using `select_related()` & `prefetch_related()`**
## **1. Understanding Reverse Relationships**
- In **OneToOneField and ForeignKey**, we can access **related data using `related_name`**.
- Example:  
  ```python
  task = Task.objects.get(id=1)
  print(task.details.priority)
  ```

✅ **The Problem?**
- Running `Task.objects.all()` and accessing `task.details.priority` in templates **runs an extra SQL query for each task**.
- **Solution:** Use **`select_related()`** to optimize queries.

---

### **2. Using `select_related()` for OneToOneField & ForeignKey**
✅ **Optimized Query (Only One SQL Query)**
```python
tasks = Task.objects.select_related('details').all()
```
- This **fetches all task details in a single SQL query** instead of separate queries for each task.

✅ **Example in `views.py`**
```python
def view_task(request):
    tasks = Task.objects.select_related('details').all()
    return render(request, "view_task.html", {"tasks": tasks})
```

✅ **Example in Template**
```html
<ul>
    {% for task in tasks %}
        <li>{{ task.title }} - {{ task.details.priority }}</li>
    {% endfor %}
</ul>
```

🚀 **`select_related()` only works on `OneToOneField` and `ForeignKey` (Parent → Child).**

---

### **3. Using `prefetch_related()` for Many-to-Many & Reverse ForeignKey**
✅ **Problem:**
- `select_related()` **doesn’t work on Many-to-Many fields**.
- **Solution:** Use **`prefetch_related()`**.

✅ **Example (Fetching Tasks for Each Project)**
```python
tasks = Project.objects.prefetch_related('task_set').all()
```

✅ **Example in `views.py`**
```python
def view_task(request):
    projects = Project.objects.prefetch_related('task_set').all()
    return render(request, "view_task.html", {"projects": projects})
```

✅ **Example in Template**
```html
<ol>
    {% for project in projects %}
        <li>{{ project.name }}
            <ul>
                {% for task in project.task_set.all %}
                    <li>{{ task.title }}</li>
                {% endfor %}
            </ul>
        </li>
    {% endfor %}
</ol>
```

🚀 **`prefetch_related()` works for both ManyToManyField & reverse ForeignKey.**

---

# **7.7 Aggregation & Annotation**
## **1. Using `aggregate()` for Total Count**
✅ **Find the total number of tasks**
```python
from django.db.models import Count

task_count = Task.objects.aggregate(task_num=Count("id"))
```

✅ **Example in `views.py`**
```python
def view_task(request):
    task_count = Task.objects.aggregate(task_num=Count("id"))
    return render(request, "view_task.html", {"task_count": task_count})
```

✅ **Example in Template**
```html
<p>Total Tasks: {{ task_count.task_num }}</p>
```

---

## **2. Using `annotate()` for Per-Object Count**
✅ **Find the number of tasks per project**
```python
project_tasks = Project.objects.annotate(task_num=Count("task"))
```

✅ **Example in `views.py`**
```python
def view_task(request):
    projects = Project.objects.annotate(task_num=Count("task"))
    return render(request, "view_task.html", {"projects": projects})
```

✅ **Example in Template**
```html
<ol>
    {% for proj in projects %}
        <li>{{ proj.name }} - Total Tasks: {{ proj.task_num }}</li>
    {% endfor %}
</ol>
```

---

### **🚀 Summary of 7.5 - 7.7**
✅ **Advanced Filtering with `Q` Lookups**  
✅ **Optimizing Queries with `select_related()` & `prefetch_related()`**  
✅ **Using `aggregate()` for total counts**  
✅ **Using `annotate()` for per-object counts**  

---

Let me know if you need **any modifications or extra explanations!** 🚀🔥