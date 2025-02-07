# **6.1 GET vs POST Methods & CSRF Token**

### **1. GET vs POST**

- **GET method**: Used when data is **not confidential** (e.g., searching, filtering).
- **POST method**: Used for **confidential data** (e.g., user login, submitting forms).
- **CSRF Token (`{% csrf_token %}`)**: Ensures data is **not sent in plain text** to the server, protecting against CSRF attacks.

---

# **6.2 Django Forms (Built-in Form Feature)**

### **1. Why Use Django Forms?**

Instead of using **HTML forms**, Django provides a **built-in form feature** to **handle validation & security** easily.

### **2. Creating `forms.py`**

In your **Django app folder**, create `forms.py`:

```python
from django import forms

class TaskForm(forms.Form):
    title = forms.CharField(max_length=250)
    description = forms.CharField()
```

### **3. Using Forms in Views (`views.py`)**

We pass the **form as context** to render it in an HTML template:

```python
from django.shortcuts import render
from .forms import TaskForm

def create_task(request):
    form = TaskForm()
    context = {
        "form": form
    }
    return render(request, 'task_form.html', context)
```

### **4. Rendering the Form in HTML (`task_form.html`)**

```html
<form action="" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Submit</button>
</form>
```

---

### **5. Handling Dynamic Fields (Fetching Data from Database)**

For fields like **`assigned_to`**, which requires data from the **Employee table**, we modify `forms.py`:

```python
from django import forms
# from tasks.models import Employee  # Uncomment if needed

class TaskForm(forms.Form):
    title = forms.CharField(max_length=250, label="Task Title")
    description = forms.CharField(widget=forms.Textarea, label="Task Description")
    due_date = forms.DateField(widget=forms.SelectDateWidget)
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        employees = kwargs.pop("employees", [])
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [(emp.id, emp.name) for emp in employees]
```

### **6. Passing Employee Data from Views (`views.py`)**

```python
from .models import Employee

def create_task(request):
    employees = Employee.objects.all()
    form = TaskForm(employees=employees)
    context = {
        "form": form
    }
    return render(request, 'task_form.html', context)
```

✅ **We inherit the `Form` class to use methods like `.as_p()`**.  
✅ **Using `super().__init__(*args, **kwargs)`** allows us to customize the form dynamically.

---

# **6.3 Saving Form Data to Database**

### **1. Updating `views.py` to Save Data**

We **store the form data** in the database using Django ORM:

```python
from django.http import HttpResponse
from .models import Task, Employee
from .forms import TaskForm

def create_task(request):
    employees = Employee.objects.all()
    form = TaskForm(employees=employees)

    if request.method == "POST":
        form = TaskForm(request.POST, employees=employees)
        if form.is_valid():
            data = form.cleaned_data  # Cleaning data to avoid HTML injection
            title = data.get('title')
            description = data.get('description')
            due_date = data.get('due_date')
            assigned_to = data.get('assigned_to')

            task = Task.objects.create(title=title, description=description, due_date=due_date)

            for emp_id in assigned_to:
                employee = Employee.objects.get(id=emp_id)
                task.assigned_to.add(employee)  # Adding to Many-to-Many table

            return HttpResponse("Task Created Successfully")

    return render(request, 'task_form.html', {"form": form})
```

✅ **We use `form.cleaned_data` to clean input before saving.**  
✅ **For Many-to-Many relations, we loop through IDs and add employees to the `assigned_to` field.**

---

# **6.4 Using `ModelForm` for Simplicity**

### **1. Why `ModelForm`?**

Instead of **writing form fields manually**, we use Django’s **`ModelForm`**, which automatically generates form fields from **models**.

### **2. Creating `TaskModelForm` in `forms.py`**

```python
from django import forms
from .models import Task

class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to']
```

### **3. Handling Form Submission in Views (`views.py`)**

```python
def create_task(request):
    form = TaskModelForm()

    if request.method == "POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():
            form.save()  # Directly saves the form data to DB
            return render(request, 'task_form.html', {'form': form, 'message': 'Task Created Successfully'})

    return render(request, 'task_form.html', {"form": form})
```

✅ **No need to manually extract and save data!**  
✅ **We can use `exclude = ['field_name']` to avoid specific fields.**

---

# **6.5 Using Widgets for Styling**

Widgets **customize how form fields render in HTML**.

### **1. Adding Widgets in `forms.py`**

```python
class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={'class': "border p-2 rounded", 'placeholder': "Enter task title"}),
            'description': forms.Textarea(attrs={'class': "border p-2 rounded", 'placeholder': "Describe your task"}),
            'due_date': forms.SelectDateWidget(attrs={'class': "border p-2 rounded"}),
            'assigned_to': forms.CheckboxSelectMultiple(attrs={'class': "border p-2 rounded"}),
        }
```

### **2. Using Tailwind CSS in `task_form.html`**

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Form</title>
    <link rel="stylesheet" href="{% static 'css/output.css' %}">
</head>
<body>
    <div class="w-1/2 mx-auto mt-8">
        <div>
            {% if message %}
                <p>{{ message }}</p>
            {% endif %}
        </div>
        <form action="" method="POST">
            {% csrf_token %}
            {{ form.as_p }}
            <button class="bg-rose-600 px-3 py-2 text-white mt-2 rounded-md" type="submit">Submit</button>
        </form>
    </div>
</body>
</html>
```

---

# **6.6 Using Mixin for Reusable Field Styles** am

Instead of writing **widget attributes manually**, we use **Mixin** for reusability.

### **1. Creating `StyledFormMixin`**

```python
class StyledFormMixin:
    default_classes = "border p-3 rounded shadow focus:outline-none focus:border-rose-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': self.default_classes,
                'placeholder': f"Enter {field.label.lower()}"})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': f"{self.default_classes}
                 resize-none", 
                'placeholder': f"Enter {field.label.lower()}", 'rows': 5})
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({'class': self.default_classes})
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({'class': "space-y-2"})
```

### **2. Applying Mixin to `TaskModelForm`**

```python
class TaskModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to']
        widgets = {'due_date': forms.SelectDateWidget, 'assigned_to': forms.CheckboxSelectMultiple}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
```

✅ **Ensures consistency in styling across all forms.**  
✅ **Avoids repetition of widget attributes.**


---

# **6.7 Understanding Method Resolution Order (MRO)**

MRO (Method Resolution Order) **determines the sequence in which Python looks up methods in a class hierarchy**.

### **1. MRO in `TaskModelForm`**

In our case, the `TaskModelForm` class inherits from **both** `StyledFormMixin` and `forms.ModelForm`:

```python
class TaskModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to']
        widgets = {'due_date': forms.SelectDateWidget, 'assigned_to': forms.CheckboxSelectMultiple}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
```

#### **MRO for `TaskModelForm`**

When Python resolves methods in this class, it follows this order:

1. `TaskModelForm` (child class)
2. `StyledFormMixin` (first parent)
3. `forms.ModelForm` (second parent)
4. `forms.BaseForm` (which `ModelForm` inherits from)
5. `object` (Python’s base class)

We can check the MRO using:

```python
print(TaskModelForm.mro())
```

### **2. How MRO Works in `TaskModelForm`**

- When calling `super().__init__(*args, **kwargs)` inside `TaskModelForm`, Python first looks for `__init__()` in `TaskModelForm` itself.
- Since `TaskModelForm` does not define its own `__init__`, Python follows MRO:
    - It **skips `StyledFormMixin`** (because `StyledFormMixin` doesn’t define `__init__`).
    - It **calls `__init__` from `forms.ModelForm`**, which initializes the form fields.
- After Django’s default form initialization, `apply_styled_widgets()` is executed from `StyledFormMixin` to apply custom styles.

### **3. Importance of MRO in Our Case**

1. **Ensures Django’s `ModelForm` logic runs first** before applying custom styles.
2. **Allows mixins (`StyledFormMixin`) to enhance the form without interfering with Django’s core logic**.
3. **Ensures multiple inheritance works correctly**, avoiding conflicts.

### **Final MRO Path**

```plaintext
TaskModelForm → StyledFormMixin → forms.ModelForm → forms.BaseForm → object
```

✅ **This order ensures that Django’s `ModelForm` setup runs first, and then our mixin applies custom styling.**

### **Final Summary**

✅ **GET vs POST Methods & CSRF Protection**  
✅ **Using Django Forms for Dynamic Data**  
✅ **Saving Form Data Using ORM**  
✅ **Using `ModelForm` to Simplify Forms**  
✅ **Applying Tailwind CSS with Widgets**  
✅ **Using Mixin to Reuse Field Styles**
✅ **MRO ensures the serial of enheritance**

Let me know if you need any modifications! 🚀