Here’s the **formatted and corrected** version of your Django template guide:

---

## **4.1 Creating Templates in Django**  
Django templates can be created in **two ways**:

### **1. Global Template Folder (Recommended for Small Projects)**  
- In the **base directory** of your project, create a folder named **`templates`**.
- In **`settings.py`**, update the `TEMPLATES` configuration:

  ```python
  TEMPLATES = [
      {
          'BACKEND': 'django.template.backends.django.DjangoTemplates',
          'DIRS': [BASE_DIR / 'templates'],  # Global templates folder
          'APP_DIRS': True,
          'OPTIONS': {
              'context_processors': [
                  'django.template.context_processors.debug',
                  'django.template.context_processors.request',
                  'django.contrib.auth.context_processors.auth',
                  'django.contrib.messages.context_processors.messages',
              ],
          },
      },
  ]
  ```

### **2. App-Specific Templates (Recommended for Larger Projects)**  
- Create a **`templates`** folder inside each Django app (e.g., `myapp/templates/myapp/`).
- No changes are needed in `settings.py` because Django automatically detects app templates when `APP_DIRS` is `True`.

---

## **4.2 Template Inheritance in Django**  
Django allows templates to **inherit from a base HTML file**, reducing repetition.

### **1. Creating a Base Template (`base.html`)**
A base template provides a structure and includes **`{% block content %}`**, where child templates insert their content.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Django Website</title>
</head>
<body>
    <header>
        <h1>Welcome to My Site</h1>
    </header>

    <main>
        {% block content %}
        <!-- Default content can go here -->
        {% endblock %}
    </main>

    <footer>
        <p>&copy; 2025 My Django Website</p>
    </footer>
</body>
</html>
```

---

### **2. Extending the Base Template in a Child Template**
A child template inherits `base.html` and replaces the `content` block.

```html
{% extends 'base.html' %}

{% block content %}
<h2>Welcome to the Home Page!</h2>
<p>This content is specific to the home page.</p>
{% endblock %}
```

- `{% extends 'base.html' %}` ensures inheritance.
- `{% block content %}...{% endblock %}` overrides content.

---

### **3. Including Reusable Templates**
To **include a reusable template** (like a navbar or footer), use `{% include %}` inside `base.html`:

```html
{% include 'navbar.html' %}
```

If `navbar.html` contains:

```html
<nav>
    <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about/">About</a></li>
        <li><a href="/contact/">Contact</a></li>
    </ul>
</nav>
```

Then **every page that extends `base.html` will include it automatically**.

---

## **4.3 Static Files in Django**
Static files (**CSS, JavaScript, images**) do not change based on user actions.

### **1. Global Static Folder (Recommended for Small Projects)**
- Create a **`static`** folder in the **base directory**.
- In `settings.py`, define:

  ```python
  STATIC_URL = '/static/'
  STATICFILES_DIRS = [
      BASE_DIR / 'static',
  ]
  ```

### **2. App-Specific Static Folder (Recommended for Larger Projects)**
- Create a `static` folder **inside each app** (e.g., `myapp/static/myapp/`).
- No changes are needed in `settings.py`.

### **Using Static Files in Templates**
To use static files (CSS/JS/images) in templates, **load the `static` tag** at the beginning:

```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/script.js' %}"></script>
<img src="{% static 'images/logo.png' %}" alt="Logo">
```

---

## **4.4 Tailwind CSS in Django**
After **Tailwind configuration**, there are **two ways** to build styles:

### **1. Using `npm run build:tailwind`**  
- This **builds** the Tailwind CSS but **does not automatically watch for changes**.

### **2. Using `npm run watch:tailwind`**  
- This **automatically watches for changes** and updates styles in real-time.

For development, **use `npm run watch:tailwind`** to see changes instantly.

---

## **4.5 Context in Django Templates**
A **context** is a **dictionary** that passes data from views to templates.

### **Example**
#### **Views (`views.py`)**
```python
def home(request):
    context = {
        'username': 'Hasan',
        'age': 25
    }
    return render(request, 'home.html', context)
```

#### **Template (`home.html`)**
```html
<h1>Welcome, {{ username }}!</h1>
<p>Your age is {{ age }}</p>
```

**Important:**  
- **Django template tags cannot be formatted into multiple lines!**
- Use `{{ variable_name }}` to display dynamic content.

---

## **4.6 Django Template Logic (Loops & Conditions)**
Django templates support:
- **`for` loops**
- **`if` conditions**
- **`with` tag** (to define variables)

### **Example**
```html
{% with count=0 %}
    {% for name in names %}
        {% if name != 'Karim' %}
            <p class="p-5 bg-red-500">{{ name }}</p>
        {% endif %} 
        {{ count|add:1 }}
    {% endfor %}
    {{ count }}
{% endwith %}
```

### **Explanation**
- `{% with count=0 %}`: Declares a variable `count`.
- `{% for name in names %}`: Loops through a list.
- `{% if name != 'Karim' %}`: Checks if the name is not `"Karim"`.
- `{{ count|add:1 }}`: Increments `count` by `1`.

---

### **Summary**
✅ **Templates can be created globally or in apps**  
✅ **Use `{% extends %}` for template inheritance**  
✅ **Use `{% include %}` for reusable components**  
✅ **Use `{% static %}` for static files like CSS & JS**  
✅ **Tailwind CSS can be built using `npm run watch:tailwind`**  
✅ **Context allows passing data from views to templates**  
✅ **Loops, conditions, and `with` tags help with template logic**  

---

Let me know if you need more details! 🚀