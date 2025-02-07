Here's the **formatted and corrected** version of your Django models and ORM guide, with all **codes clearly visible** and properly structured.

---

## **5.3 Connecting PostgreSQL with Django**  
To connect **PostgreSQL** with our Django project, we need to **modify `settings.py`**:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'task_management',  # Change this to your database name
        'USER': 'postgres',  # Change this to your database user
        'PASSWORD': '1234',  # Change this to your PostgreSQL password
        'HOST': 'localhost',
        'PORT': '5432'
    }
}
```
- The **database name (`NAME`) and password (`PASSWORD`)** should match what you set in PostgreSQL.

---

## **5.4 Creating Database Tables in Django**
### **1. Defining Models in `models.py`**  
Django stores data using **models**, where each class represents a database table. We define fields using Django’s **model field types** ([Reference](https://docs.djangoproject.com/en/5.1/ref/models/fields/#field-types)).

Example:
```python
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
```

### **2. Making Migrations**
- **Step 1:** Convert models to migration files:
  ```bash
  python manage.py makemigrations
  ```
- **Step 2:** Apply the migrations to create tables in PostgreSQL:
  ```bash
  python manage.py migrate
  ```
- **Table Naming Convention:**  
  Django creates tables using the format **`appname_modelname`**.  
  Example:
  - App name: `tasks`
  - Model name: `Task`
  - Table created in PostgreSQL: **`tasks_task`**

---

## **5.5 Handling Relationships in Models**
### **1. Dropdown Choices in Models**
We can create **dropdown choices** using tuples inside `CharField`:

```python
class TaskDetail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_OPTIONS = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low')
    )

    assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
```
✅ **Using variables for choices ensures easier updates.**

### **2. One-to-One Relationship**
One-to-one relationships are defined using `OneToOneField`:
```python
task = models.OneToOneField(Task, on_delete=models.CASCADE)
```
- **`on_delete`** defines what happens when the parent is deleted:
  - `CASCADE` → Delete child records  
  - `PROTECT` → Prevent deletion  
  - `RESTRICT` → Prevent deletion (Django 3.1+)  
  - `SET_NULL` → Set foreign key to `NULL`  
  - `SET_DEFAULT` → Assign a default value  
  - `DO_NOTHING` → Do nothing  

---

## **5.6 Using Django Shell for Database Operations**
Django Shell lets us interact with the database using Python.  

### **1. Entering Django Shell**
```bash
python manage.py shell
```

### **2. Creating Objects in Two Ways**
#### **Method 1: Using `.save()`**
```python
t = Task(title="Low Priority Task", description="Test task", due_date="2025-02-07")
t.save()
```
#### **Method 2: Using `.create()` (Auto-Saves)**
```python
t = Task.objects.create(title="High Priority Task", description="Test task", due_date="2025-02-08")
```

### **3. Fetching Objects**
```python
task = Task.objects.get(id=1)  # Get task with ID = 1
```

### **4. Creating Related Objects**
Since `TaskDetail` depends on `Task`, we **must use an existing `Task` instance**:
```python
task_detail = TaskDetail.objects.create(task=task, assigned_to="Me", priority="L")
```

### **5. Understanding Django ORM**
- `.create()` → Equivalent to **SQL `INSERT`**
- `.get()` → Equivalent to **SQL `SELECT`**
- This is called **Object-Relational Mapping (ORM)**.

---

## **5.7 Many-to-One Relationship (`ForeignKey`)**
### **1. Creating a `Project` Model**
```python
class Project(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
```
### **2. Linking `Task` to `Project` (Many-to-One)**
A project can have multiple tasks, so we **add `ForeignKey` in `Task`**:
```python
class Task(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
```
- **Order Matters:**  
  - The parent model (`Project`) **must be declared before** the dependent model (`Task`).
  - If it’s declared later, use **"Project" (string format)** inside `ForeignKey`.

### **3. Handling Migration Errors**
- If `Task` already contains data and we add `project`, migration will fail.  
  ✅ **Solution 1:** Make `project` nullable:
  ```python
  project = models.ForeignKey("Project", on_delete=models.CASCADE, null=True, blank=True)
  ```
  ✅ **Solution 2:**  
  - Migrate `Project` first.  
  - Add data in `Project`.  
  - Then migrate `Task` with `ForeignKey`.

### **4. Fetching Data from `Project`**
```python
>>> project = Project.objects.all()
>>> project.first().id
1  # ID of the first project
```

---

## **5.8 Many-to-Many Relationship**
### **1. Defining Employee and Task Models**
```python
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
```
```python
class Task(models.Model):
    assigned_to = models.ManyToManyField(Employee)
```
### **2. How Many-to-Many Works**
- **Django automatically creates a junction table** with `employee_id` and `task_id`.

### **3. Querying Many-to-Many Relations**
```python
task.assigned_to.all()  # Get all employees assigned to a task
```

---

## **5.9 Reverse Relationships & `related_name`**
### **1. One-to-One Reverse Relation (`TaskDetail` → `Task`)**
- By default, Django creates a **hidden field** in the parent (`Task`), named after the child model:
```python
Task.objects.get(id=1).taskdetail  # Get TaskDetail for Task ID=1
```
- **Customizing the Field Name (`related_name`)**:
```python
task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name="details")
```
```python
Task.objects.get(id=1).details  # Now "details" is used instead of "taskdetail"
```

---

### **2. Many-to-Many Reverse Relation (`Employee` ↔ `Task`)**
- By default, Django adds `_set` to the child model’s name:
```python
Employee.objects.get(id=1).task_set.all()  # Get tasks assigned to an employee
```
- **Using `related_name` to Customize**:
```python
assigned_to = models.ManyToManyField(Employee, related_name="tasks")
```
```python
Employee.objects.get(id=1).tasks.all()  # Now "tasks" is used instead of "task_set"
```

---

### **3. Many-to-One Reverse Relation (`Project` → `Task`)**
- By default, Django names it **`task_set`**:
```python
Project.objects.get(id=1).task_set.all()  # Get all tasks under project ID=1
```
- **Using `related_name`**:
```python
project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name="tasks")
```
```python
Project.objects.get(id=1).tasks.all()  # Now "tasks" is used instead of "task_set"
```

---

### **Final Summary**
✅ **PostgreSQL setup in `settings.py`**  
✅ **Migrations convert Python models into SQL tables**  
✅ **One-to-One, Many-to-One, and Many-to-Many relationships explained**  
✅ **Using `related_name` for reverse relationships**  

Let me know if you need further refinements! 🚀