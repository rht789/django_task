
# **Module 13: Details view and Media Files**  
This module covers updates to the TaskMaster Django application, including a dynamic homepage and navbar, multilevel template inheritance, media integration, default images, dynamic status changes, and role-based dashboards. Below is a detailed guide with **why** each step is implemented, **example code**, and additional notes.

---

## **13.1 Homepage and Dynamic Navbar**  
The homepage and navigation bar were updated to be reusable across all pages, with distinct authenticated and non-authenticated states for the navbar, housed in the `core` app’s templates.

### **Why We Updated the Homepage and Navbar**  
- ✅ **Consistency**: A shared navbar ensures a uniform look and navigation experience across the app.  
- ✅ **Role Awareness**: Separate navbars for authenticated (e.g., Dashboard, Tasks) and non-authenticated (e.g., Features, Sign Up) users improve usability.  
- ✅ **Engagement**: A revamped homepage with a hero, features, and CTA drives user interest and adoption.

### **Base Template: `base.html`**  
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{% block title %}{% endblock title %}</title>
    <script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=Noto+Sans+Bengali:wght@100..900&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="{% static 'css/output.css' %}">
    <style>body { font-family: "Inter", sans-serif; }</style>
  </head>
  <body class="font-sans bg-gray-100">
    {% if request.user.is_authenticated %}
        {% include "logged_nav.html" %}
    {% else %}
        {% include "non_logged_nav.html" %}
    {% endif %}
    <main>{% block content %}{% endblock content %}</main>
    <footer class="bg-gray-800 text-white py-12">
      <div class="container mx-auto px-6">
        <div class="flex flex-wrap justify-between">
          <div class="w-full md:w-1/4 mb-8 md:mb-0">
            <h3 class="text-lg font-semibold mb-4">TaskMaster</h3>
            <p class="text-gray-400">Empowering teams with efficient task management solutions.</p>
          </div>
          <div class="w-full md:w-1/4 mb-8 md:mb-0">
            <h4 class="text-lg font-semibold mb-4">Quick Links</h4>
            <ul class="text-gray-400 space-y-2">
              <li><a href="#" class="hover:text-white">Home</a></li>
              <li><a href="#" class="hover:text-white">Features</a></li>
              <li><a href="#" class="hover:text-white">Pricing</a></li>
              <li><a href="#" class="hover:text-white">Contact</a></li>
            </ul>
          </div>
          <div class="w-full md:w-1/4 mb-8 md:mb-0">
            <h4 class="text-lg font-semibold mb-4">Connect</h4>
            <ul class="text-gray-400 space-y-2">
              <li><a href="#" class="hover:text-white">Twitter</a></li>
              <li><a href="#" class="hover:text-white">LinkedIn</a></li>
              <li><a href="#" class="hover:text-white">Facebook</a></li>
            </ul>
          </div>
          <div class="w-full md:w-1/4">
            <h4 class="text-lg font-semibold mb-4">Newsletter</h4>
            <form class="flex">
              <input type="email" placeholder="Your email" class="w-full px-3 py-2 text-gray-700 bg-gray-200 rounded-l-md focus:outline-none" required />
              <button type="submit" class="bg-purple-500 text-white px-4 py-2 rounded-r-md hover:bg-purple-600 transition duration-300">Subscribe</button>
            </form>
          </div>
        </div>
        <div class="border-t border-gray-700 mt-12 pt-8 text-sm text-center text-gray-400">
          © 2023 TaskMaster. All rights reserved.
        </div>
      </div>
    </footer>
    <script>
        document.getElementById("menu-toggle").addEventListener("click", function () {
          document.getElementById("mobile-menu").classList.toggle("hidden");
        });
        document.getElementById("user-menu-button").addEventListener("click", function () {
          document.getElementById("user-menu").classList.toggle("hidden");
        });
        window.addEventListener("click", function (e) {
          if (!document.getElementById("user-menu-button").contains(e.target)) {
            document.getElementById("user-menu").classList.add("hidden");
          }
        });
    </script>
  </body>
</html>
```
- **Notes**:  
  - **Dynamic Navbar**: Uses `{% if request.user.is_authenticated %}` to switch between `logged_nav.html` and `non_logged_nav.html`.  
  - **Fonts**: Integrates Google Fonts (`Inter`) and FontAwesome for icons.  
  - **Footer**: Adds branding, links, and a newsletter form for engagement.

### **Homepage: `home.html`**  
```html
{% extends "base.html" %}
{% block content %}
<!-- Hero Section -->
<section class="bg-purple-600 text-white py-32 md:py-40">
    <div class="container mx-auto px-6 text-center">
      <h1 class="text-4xl md:text-5xl font-bold mb-6">Streamline Your Workflow with TaskMaster</h1>
      <p class="text-xl mb-12">Empower your team with our intuitive task management solution</p>
      <a href="#" class="bg-white text-purple-600 px-8 py-4 rounded-md font-semibold text-lg hover:bg-gray-100 transition duration-300">Get Started</a>
    </div>
</section>
<!-- Features Section -->
<section class="py-24 md:py-32">
    <div class="container mx-auto px-6">
      <h2 class="text-3xl font-bold text-center mb-16">Tailored for Every Role</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-12">
        <!-- Admin Card -->
        <div class="bg-white rounded-lg shadow-md p-8">
          <h3 class="text-2xl font-semibold mb-6">Admin</h3>
          <ul class="list-disc list-inside text-gray-600 space-y-3">
            <li>Manage user roles and permissions</li>
            <li>Generate comprehensive reports</li>
            <li>Configure system-wide settings</li>
            <li>Monitor team performance</li>
          </ul>
        </div>
        <!-- Manager Card -->
        <div class="bg-white rounded-lg shadow-md p-8">
          <h3 class="text-2xl font-semibold mb-6">Manager</h3>
          <ul class="list-disc list-inside text-gray-600 space-y-3">
            <li>Create and assign tasks to employees</li>
            <li>Track project progress in real-time</li>
            <li>Set deadlines and priorities</li>
            <li>Generate team performance reports</li>
          </ul>
        </div>
        <!-- Employee Card -->
        <div class="bg-white rounded-lg shadow-md p-8">
          <h3 class="text-2xl font-semibold mb-6">Employee</h3>
          <ul class="list-disc list-inside text-gray-600 space-y-3">
            <li>View and manage assigned tasks</li>
            <li>Collaborate with team members</li>
            <li>Update task status and progress</li>
            <li>Track personal productivity</li>
          </ul>
        </div>
      </div>
    </div>
</section>
<!-- Call to Action -->
<section class="bg-gray-200 py-24 md:py-32">
    <div class="container mx-auto px-6 text-center">
      <h2 class="text-3xl font-bold mb-6">Ready to Boost Your Team's Productivity?</h2>
      <p class="text-xl mb-12">Join thousands of organizations already using TaskMaster</p>
      <a href="#" class="bg-purple-500 text-white px-8 py-4 rounded-md font-semibold text-lg hover:bg-purple-600 transition duration-300">Start Free Trial</a>
    </div>
</section>
{% endblock %}
```
- **Notes**:  
  - **Hero**: Promotes TaskMaster with a prominent CTA.  
  - **Features**: Highlights role-specific benefits using a responsive grid.  
  - **CTA**: Encourages trial sign-ups with a styled button.

### **Authenticated Navbar: `logged_nav.html`**  
```html
<header class="bg-white shadow-md">
    <nav class="container mx-auto px-6 py-3">
      <div class="flex justify-between items-center">
        <a href="index.html" class="text-xl font-bold text-gray-800">Taskify</a>
        <div class="hidden md:flex space-x-4">
          <a href="{% url 'manager_dashboard' %}" class="text-gray-600 hover:text-gray-800">Dashboard</a>
          <a href="#" class="text-gray-600 hover:text-gray-800">Tasks</a>
          <a href="{% url 'group-list' %}" class="text-gray-600 hover:text-gray-800">Tasks</a>
          <a href="{% url 'create_task' %}" class="text-gray-600 hover:text-gray-800">Create Task</a>
        </div>
        <div class="flex items-center">
          <div class="relative">
            <button id="user-menu-button" class="flex items-center focus:outline-none">
              <img class="h-8 w-8 rounded-full object-cover" src="https://placekitten.com/100/100" alt="User avatar" />
            </button>
            <div id="user-menu" class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 hidden">
              <a href="{% url 'admin-dashboard' %}" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Dashboard</a>
              <form method="post" action="{% url 'sign-out' %}">
                  {% csrf_token %}
                <button class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Logout</button>
              </form>
            </div>
          </div>
          <div class="md:hidden ml-4">
            <button id="menu-toggle" class="text-gray-600 hover:text-gray-800 focus:outline-none">
              <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path>
              </svg>
            </button>
          </div>
        </div>
      </div>
      <div id="mobile-menu" class="md:hidden hidden mt-4">
        <a href="#" class="block py-2 text-gray-600 hover:text-gray-800">Dashboard</a>
        <a href="#" class="block py-2 text-gray-600 hover:text-gray-800">Tasks</a>
        <a href="#" class="block py-2 text-gray-600 hover:text-gray-800">Groups</a>
        <a href="#" class="block py-2 text-gray-600 hover:text-gray-800">Create Group</a>
      </div>
    </nav>
</header>
```
- **Notes**:  
  - **Dropdown**: User avatar triggers a menu with Dashboard and Logout options.  
  - **Mobile**: Hamburger menu toggles navigation for small screens.

### **Non-Authenticated Navbar: `non_logged_nav.html`**  
```html
<header class="bg-white shadow-md">
    <nav class="container mx-auto px-6 py-3">
      <div class="flex justify-between items-center">
        <div class="text-xl font-bold text-gray-800">TaskMaster</div>
        <div class="hidden md:flex space-x-4">
          <a href="#" class="text-gray-600 hover:text-gray-800">Features</a>
          <a href="#" class="text-gray-600 hover:text-gray-800">Pricing</a>
          <a href="#" class="text-gray-600 hover:text-gray-800">About</a>
          <a href="#" class="text-gray-600 hover:text-gray-800">Contact</a>
        </div>
        <div class="md:hidden">
          <button id="menu-toggle" class="text-gray-600 hover:text-gray-800 focus:outline-none">
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path>
            </svg>
          </button>
        </div>
        <div class="flex gap-1">
          <a href="{% url 'sign-in' %}" class="hidden md:block bg-purple-500 text-white px-4 py-2 rounded-md hover:bg-purple-600 transition duration-300">Sign In</a>
          <a href="{% url 'sign-up' %}" class="hidden md:block text-purple-500 bg-white border border-purple-500 px-4 py-2 rounded-md hover:bg-purple-600 hover:text-white transition duration-300">Sign Up</a>
        </div>
      </div>
      <div id="mobile-menu" class="md:hidden hidden mt-4">
        <a href="#" class="block py-2 text-gray-600 hover:text-gray-800">Features</a>
        <a href="#" class="block py-2 text-gray-600 hover:text-gray-800">Pricing</a>
        <a href="#" class="block py-2 text-gray-600 hover:text-gray-800">About</a>
        <a href="#" class="block py-2 text-gray-600 hover:text-gray-800">Contact</a>
        <a href="#" class="block py-2 text-gray-600 hover:text-gray-800">Sign In</a>
        <a href="#" class="block py-2 text-gray-600 hover:text-gray-800">Sign Up</a>
      </div>
    </nav>
</header>
```
- **Notes**:  
  - **Links**: Focuses on marketing pages and authentication options.  
  - **Responsive**: Mobile menu mirrors desktop links.

### **User Templates (in `users` app)**  
#### **`register.html`**  
```html
{% extends "base.html" %}
{% block content %}
    <div class='w-1/2 mx-auto my-9'>
        {% if form.non_field_errors %}
            {% for error in form.non_field_errors %}
                {{ error }}
            {% endfor %}
        {% endif %}
        <form action="" method="POST">
            {% csrf_token %}
            {% for field in form %}
               <p>
                    <label for="{{ field.id_for_label }}"> {{field.label}} </label>
                    {{ field }}
                    {% if field.errors %}
                            <ul>
                                {% for error in field.errors %}
                                <li>{{error}}</li>
                                {% endfor %}
                            </ul>
                    {% endif %}
               </p>
            {% endfor %}
            <button class="bg-purple-500 px-2 py-1 rounded text-white mt-3" type="submit">Sign Up</button>
        </form>
    </div>
{% endblock content %}
```
- **Notes**:  
  - **Validation**: Displays form errors for user feedback.  
  - **Styling**: Uses Tailwind classes for a clean signup form.

#### **`signin.html`**  
```html
{% extends "base.html" %}
{% block content %}
    <div class='mx-auto w-1/2 my-9'>
        {% if messages %}
            {% for message in messages %}
                <div class="px-2 py-1 {% if message.tags == 'success' %}bg-green-500{% endif %} ">{{message}}</div>
            {% endfor %}
        {% endif %}
        <form method='POST'>
            {% csrf_token %}
            {{ form }}
            <button class='bg-purple-500 px-2 py-1 rounded text-white mt-3' type="submit">Sign In</button>
        </form>
    </div>
{% endblock content %}
```
- **Notes**:  
  - **Messages**: Shows success/error feedback post-login.  
  - **Simplicity**: Renders the form directly with minimal markup.

---

## **13.2 Multilevel Template Inheritance**  
Template inheritance was implemented from `base.html` to `dashboard.html` in the `tasks` app to create a reusable dashboard structure.

### **Why Use Template Inheritance**  
- ✅ **Reusability**: Extends `base.html` to maintain a consistent layout.  
- ✅ **Flexibility**: Allows nested blocks (e.g., `tasks`) for further customization.  
- ✅ **Clarity**: Displays task statistics in a grid for quick insights.

### **Dashboard Template: `dashboard.html`**  
```html
{% extends "base.html" %}
{% block content %}
<div class="w-[1470px] mx-auto my-8 bg-gray-100">
  <div class="grid grid-cols-4 gap-6">
    <!-- Total Task -->
    <a href="{% url 'manager_dashboard' %}">
      <div class="bg-white rounded-xl p-6 shadow-sm">
        <h3 class="text-sm font-medium text-gray-500 mb-4">Total Task</h3>
        <div class="flex justify-between items-start">
          <div>
            <p class="text-3xl font-semibold mb-1">{{counts.total_task}}</p>
            <p class="text-gray-500 text-sm">111 Last Month</p>
          </div>
          <div class="bg-blue-100 p-3 rounded-full">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-blue-600 font-semibold">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.666 3.888A2.25 2.25 0 0 0 13.5 2.25h-3c-1.03 0-1.9.693-2.166 1.638m7.332 0c.055.194.084.4.084.612v0a.75.75 0 0 1-.75.75H9a.75.75 0 0 1-.75-.75v0c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 0 1-2.25 2.25H6.75A2.25 2.25 0 0 1 4.5 19.5V6.257c0-1.108.806-2.057 1.907-2.185a48.208 48.208 0 0 1 1.927-.184" />
            </svg>
          </div>
        </div>
      </div>
    </a>
    <!-- Completed Task -->
    <a href="{% url 'manager_dashboard' %}?type=completed">
      <div class="bg-white rounded-xl p-6 shadow-sm">
        <h3 class="text-sm font-medium text-gray-500 mb-4">Completed Task</h3>
        <div class="flex justify-between items-start">
          <div>
            <p class="text-3xl font-semibold mb-1">{{counts.completed_task}}</p>
            <p class="text-gray-500 text-sm">111 Last Month</p>
          </div>
          <div class="bg-green-100 p-3 rounded-full">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-green-600">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>
          </div>
        </div>
      </div>
    </a>
    <!-- Task in Progress -->
    <a href="{% url 'manager_dashboard' %}?type=in_progress">
      <div class="bg-white rounded-xl p-6 shadow-sm">
        <h3 class="text-sm font-medium text-gray-500 mb-4">Task in Progress</h3>
        <div class="flex justify-between items-start">
          <div>
            <p class="text-3xl font-semibold mb-1">{{counts.in_progress_task}}</p>
            <p class="text-gray-500 text-sm">111 Last Month</p>
          </div>
          <div class="bg-yellow-100 p-3 rounded-full">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-yellow-600">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>
          </div>
        </div>
      </div>
    </a>
    <!-- Todos -->
    <a href="{% url 'manager_dashboard' %}?type=pending">
      <div class="bg-white rounded-xl p-6 shadow-sm">
        <h3 class="text-sm font-medium text-gray-500 mb-4">Todos</h3>
        <div class="flex justify-between items-start">
          <div>
            <p class="text-3xl font-semibold mb-1">{{counts.pending_task}}</p>
            <p class="text-gray-500 text-sm">111 Last Month</p>
          </div>
          <div class="bg-purple-100 p-3 rounded-full">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-purple-600">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.666 3.888A2.25 2.25 0 0 0 13.5 2.25h-3c-1.03 0-1.9.693-2.166 1.638m7.332 0c.055.194.084.4.084.612v0a.75.75 0 0 1-.75.75H9a.75.75 0 0 1-.75-.75v0c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 0 1-2.25 2.25H6.75A2.25 2.25 0 0 1 4.5 19.5V6.257c0-1.108.806-2.057 1.907-2.185a48.208 48.208 0 0 1 1.927-.184" />
            </svg>
          </div>
        </div>
      </div>
    </a>
  </div>
  <div class="mb-4">
    {% if messages %}
        {% for message in messages %}
            <div class="px-2 py-1 {% if message.tags == 'success' %}bg-green-500{% endif %} {% if message.tags == 'error' %}bg-red-500{% endif %}">{{message}}</div>
        {% endfor %}
    {% endif %}
  </div>
  {% block tasks %}{% endblock tasks %}
</div>
{% endblock content %}
```
- **Notes**:  
  - **Grid Layout**: Displays task stats (Total, Completed, In Progress, Todos) with links to filtered views.  
  - **Icons**: SVG icons enhance visual appeal.  
  - **Messages**: Shows success/error feedback.

---

## **13.2-13.3 Task Details and Database Changes**  
Updated the database by removing the `Employee` model and added a detailed task view with a template, view, and URL.

### **Why Make These Changes**  
- ✅ **Simplification**: Replacing `Employee` with a `ManyToManyField` to `User` reduces complexity.  
- ✅ **Detail View**: Provides a comprehensive task overview (team, status, assets) for better management.

### **Model Changes: `Task`**  
```python
class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed')
    ]
    project = models.ForeignKey("Project", on_delete=models.CASCADE, default=1)
    assigned_to = models.ManyToManyField(User, related_name='tasks')
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
```
- **Notes**:  
  - **`assigned_to`**: Links tasks directly to users, eliminating the need for a separate `Employee` model.

### **Task Details Template: `task_details.html`**  
```html
{% extends "base.html" %}
{% block title %}{{task.title}}-Task Details{% endblock title %}
{% block content %}
<div class="container mx-auto px-4 py-8 max-w-7xl">
    <h1 class="text-3xl font-bold mb-6">{{task.title}}</h1>
    <!-- Navigation Tabs -->
    <div class="flex gap-4 mb-8 border-b">
      <button class="px-4 py-2 bg-blue-50 text-blue-600 rounded-t-lg flex items-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
        </svg>
        Task Detail
      </button>
      <div class="flex items-center gap-2">
        <form method='post'>
            {% csrf_token %}
            <select name="task_status" id="task_status" class="px-4 py-2 border rounded-md">
                {% for value, label in status_choices %}
                    <option value="{{ value }}">{{label}}</option>
                {% endfor %}
            </select>
            <button class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600" type="submit">Change Status</button>
        </form>
      </div>
    </div>
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Main Content -->
      <div class="lg:col-span-2">
        <div class="bg-white p-6 rounded-lg shadow-sm">
          <!-- Status Tags -->
          <div class="flex gap-3 mb-6">
            <span class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">{{task.details.get_priority_display|upper}} PRIORITY</span>
            <span class="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">{{task.status}}</span>
          </div>
          <!-- Creation Date -->
          <div class="text-gray-600 mb-6">{{task.created_at}}</div>
          <!-- Task Team -->
          <div class="mb-9">
            <h2 class="text-xl font-bold mb-4">TASK TEAM</h2>
            <div class="space-y-4">
              {% for emp in task.assigned_to.all %}
                <div class="flex items-center gap-4">
                  <div class="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-white">
                    {{emp.first_name|slice:':1'}}{{emp.last_name|slice:":1"}}
                  </div>
                  <div>
                    <div class="font-semibold">{{emp.first_name}} {{emp.last_name}}</div>
                    <div class="text-gray-600">{{emp.groups.first.name|default:"No Role"}}</div>
                  </div>
                </div>
              {% endfor %}
            </div>
          </div>
          <div>
            <a href='{% url "update_task" task.id %}' class="px-2 py-1 bg-green-500">Edit</a>
            <form action='{% url "delete_task" task.id %}' method='POST'>
              {% csrf_token %}
              <button class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600" type="submit">Delete Task</button>
            </form>
          </div>
        </div>
      </div>
      <!-- Sidebar -->
      <div class="lg:col-span-1">
        <!-- Task Description -->
        <div class="bg-white p-6 rounded-lg shadow-sm mb-6">
          <h2 class="text-xl font-bold mb-4">TASK DESCRIPTION</h2>
          <p class="text-gray-600">{{task.description}}</p>
        </div>
        <!-- Assets -->
        <div class="bg-white p-6 rounded-lg shadow-sm">
          <h2 class="text-xl font-bold mb-4">ASSETS</h2>
          <div class="space-y-4">
            <img src={{task.details.assets.url}} alt="Task Manager App Screenshot 1" class="w-full rounded-lg" />
          </div>
        </div>
      </div>
    </div>
</div>
{% endblock content %}
```
- **Notes**:  
  - **Status Dropdown**: Populates from `status_choices` (later handled in 13.8).  
  - **Task Team**: Lists assigned users with initials and roles.  
  - **Assets**: Displays images linked to `task.details.assets`.

### **View: `task_details`**  
```python
def task_details(request, task_id):
    task = Task.objects.get(id=task_id)
    return render(request, 'task_details.html', {'task': task})
```

### **URL: `urls.py`**  
```python
path('task/<int:task_id>/details', task_details, name='task_details'),
```

---

## **13.3-13.4 Add Media in Templates**  
Added media upload functionality to tasks, including models, forms, settings, and views.

### **Why Add Media**  
- ✅ **Context**: Images provide visual context for tasks (e.g., screenshots).  
- ✅ **Flexibility**: Optional uploads with proper handling enhance usability.

### **Model Updates: `tasks/models.py`**  
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
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='details')
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
    assets = models.ImageField(upload_to='tasks_asset', blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Details from Task {self.task}"
```
- **Notes**:  
  - **`assets`**: `ImageField` for uploads; requires `Pillow` (`pip install Pillow`).  
  - **`upload_to`**: Stores files in `media/tasks_asset/`.  
  - **`blank=True, null=True`**: Makes uploads optional.

### **Forms: `tasks/forms.py`**  
```python
class TaskModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to', 'project']
        widgets = {
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple
        }

class TaskDetailModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = TaskDetail
        fields = ['priority', 'notes', 'assets']

class StyledFormMixin:
    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()
    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': self.default_classes, 'placeholder': f"Enter {field.label}"})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': f"{self.default_classes} resize-none", 'placeholder': f"Enter {field.label}", 'rows': 5})
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({"class": "border-2 border-gray-300 bg-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"})
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({'class': "space-y-2"})
            else:
                field.widget.attrs.update({'class': self.default_classes})
```
- **Notes**:  
  - **`StyledFormMixin`**: Applies consistent Tailwind styling to forms.  
  - **`TaskDetailModelForm`**: Includes `assets` for image uploads.

### **Settings: `settings.py`**  
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```
- **Notes**:  
  - **`MEDIA_URL`**: URL prefix for serving media (e.g., `/media/`).  
  - **`MEDIA_ROOT`**: Directory for uploaded files (e.g., `<project_root>/media/`).

### **URLs: `base urls.py`**  
```python
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
- **Notes**:  
  - Serves media files during development.

### **Task Form Template: `task_form.html`**  
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Form</title>
    <link rel="stylesheet" href="{% static "css/output.css" %}">
</head>
<body>
    <div class="w-1/2 mx-auto mt-8">
        <div>
        {% if messages %}
            {% for message in messages %}
                <div class="px-2 py-1 {% if message.tags == 'success' %}bg-green-500{% endif %} ">{{message}}</div>
            {% endfor %}
        {% endif %}
        </div>
        <form method="POST" enctype="multipart/form-data">
            {% csrf_token %}
            {{ task_form.as_p }}
            {{ taskdetail_form.as_p }}
            <button class="mb-5 bg-rose-600 px-3 py-2 text-white mt-2 rounded-md" type="submit">Submit</button>
        </form>
    </div>
</body>
</html>
```
- **Notes**:  
  - **`enctype="multipart/form-data"`**: Essential for file uploads.

### **Views: `tasks/views.py`**  
```python
@login_required
@permission_required("tasks.add_task", login_url='no-permission')
def create_task(request):
    task_form = TaskModelForm()
    taskdetail_form = TaskDetailModelForm()
    if request.method == "POST":
        task_form = TaskModelForm(request.POST)
        taskdetail_form = TaskDetailModelForm(request.POST, request.FILES)
        if task_form.is_valid() and taskdetail_form.is_valid():
            task = task_form.save()
            taskdetail = taskdetail_form.save(commit=False)
            taskdetail.task = task
            taskdetail.save()
            messages.success(request, "Task Created Successfully")
            return redirect('create_task')
    context = {"task_form": task_form, "taskdetail_form": taskdetail_form}
    return render(request, 'task_form.html', context)
```
- **Notes**:  
  - **`request.FILES`**: Captures uploaded media; without it, files wouldn’t be processed.

---

## **13.8 Default Image and Dynamic Status Change**  
Added a default image for tasks without assets and implemented dynamic status updates.

### **Why Add These Features**  
- ✅ **Default Image**: Ensures a fallback visual if no image is uploaded.  
- ✅ **Dynamic Status**: Allows real-time task status changes without page reloads.

### **Model Update: `TaskDetail`**  
```python
class TaskDetail(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='details')
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default='L')
    assets = models.ImageField(upload_to='tasks_asset', blank=True, null=True, default="tasks_asset/default_img.jpg")
    notes = models.TextField(blank=True, null=True)
```
- **Notes**:  
  - **`default="tasks_asset/default_img.jpg"`**: Sets a default image.

### **Updated Template: `task_details.html`**  
```html
{% extends "base.html" %}
{% block title %}{{task.title}}-Task Details{% endblock title %}
{% block content %}
<div class="container mx-auto px-4 py-8 max-w-7xl">
    <h1 class="text-3xl font-bold mb-6">{{task.title}}</h1>
    <div class="flex gap-4 mb-8 border-b">
      <button class="px-4 py-2 bg-blue-50 text-blue-600 rounded-t-lg flex items-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
        </svg>
        Task Detail
      </button>
      <div class="flex items-center gap-2">
        <form method='post'>
            {% csrf_token %}
            <select name="task_status" id="task_status" class="px-4 py-2 border rounded-md">
                {% for value, label in status_choices %}
                    <option value="{{ value }}">{{label}}</option>
                {% endfor %}
            </select>
            <button class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600" type="submit">Change Status</button>
        </form>
      </div>
    </div>
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <div class="bg-white p-6 rounded-lg shadow-sm">
          <div class="flex gap-3 mb-6">
            <span class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">{{task.details.get_priority_display|upper}} PRIORITY</span>
            <span class="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">{{task.status}}</span>
          </div>
          <div class="text-gray-600 mb-6">{{task.created_at}}</div>
          <div class="mb-9">
            <h2 class="text-xl font-bold mb-4">TASK TEAM</h2>
            <div class="space-y-4">
              {% for emp in task.assigned_to.all %}
                <div class="flex items-center gap-4">
                  <div class="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-white">
                    {{emp.first_name|slice:':1'}}{{emp.last_name|slice:":1"}}
                  </div>
                  <div>
                    <div class="font-semibold">{{emp.first_name}} {{emp.last_name}}</div>
                    <div class="text-gray-600">{{emp.groups.first.name|default:"No Role"}}</div>
                  </div>
                </div>
              {% endfor %}
            </div>
          </div>
          <div class="flex gap-4">
            <a href='{% url "update_task" task.id %}' class="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600">Edit Task</a>
            <form action='{% url "delete_task" task.id %}' method='POST'>
              {% csrf_token %}
              <button class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600" type="submit">Delete Task</button>
            </form>
          </div>
        </div>
      </div>
      <div class="lg:col-span-1">
        <div class="bg-white p-6 rounded-lg shadow-sm mb-6">
          <h2 class="text-xl font-bold mb-4">TASK DESCRIPTION</h2>
          <p class="text-gray-600">{{task.description}}</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-sm">
          <h2 class="text-xl font-bold mb-4">ASSETS</h2>
          <div class="space-y-4">
            <img src={{task.details.assets.url}} alt="Task Manager App Screenshot 1" class="w-full rounded-lg" />
          </div>
        </div>
      </div>
    </div>
</div>
{% endblock content %}
```
- **Notes**:  
  - **Buttons**: Edit and Delete buttons styled with Tailwind for consistency.  
  - **Status Form**: Now functional with view updates.

### **Updated View: `task_details`**  
```python
@login_required
@permission_required("tasks.view_task", login_url='no-permission')
def task_details(request, task_id):
    task = Task.objects.get(id=task_id)
    status_choices = Task.STATUS_CHOICES
    if request.method == "POST":
        changed_status = request.POST.get('task_status')
        task.status = changed_status
        task.save()
        return redirect('task_details', task.id)
    return render(request, 'task_details.html', {'task': task, 'status_choices': status_choices})
```
- **Notes**:  
  - **`status_choices`**: Passed to template for dropdown.  
  - **POST Handling**: Updates `task.status` and redirects.

---

## **13.9 Role-Based Dashboard**  
Implemented a role-based dashboard redirect based on user groups (Admin, Manager, Employee).

### **Why Implement Role-Based Dashboards**  
- ✅ **Personalization**: Users see dashboards tailored to their roles.  
- ✅ **Security**: Restricts access to authorized views only.

### **View: `dashboard`**  
```python
@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect('manager_dashboard')
    elif is_employee(request.user):
        return redirect('employee_dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')
    return redirect('no-permission')
```
- **Notes**:  
  - **Role Checks**: Uses `is_manager`, `is_employee`, and `is_admin` from `views.py`.

### **URL: `urls.py`**  
```python
path('dashboard', dashboard, name='dashboard')
```

### **Navbar Update: `logged_nav.html`**  
```html
<a href="{% url 'dashboard' %}" class="text-gray-600 hover:text-gray-800">Dashboard</a>
```
- **Notes**:  
  - Links to the generic `dashboard` view, which redirects based on role.

---

# **Final Summary**  
1. **Homepage & Navbar**: Updated for consistency and role-aware navigation with `base.html`, `home.html`, `logged_nav.html`, and `non_logged_nav.html`.  
2. **Template Inheritance**: `dashboard.html` extends `base.html` for a modular dashboard with task stats.  
3. **Task Details**: Added `task_details.html` with team, status, and assets; removed `Employee` model for simplicity.  
4. **Media Integration**: Added `assets` to `TaskDetail`, with forms, settings, and views supporting uploads.  
5. **Default Image & Status**: Set a default image and enabled dynamic status changes in `task_details`.  
6. **Role-Based Dashboards**: Redirects users to appropriate dashboards based on their group.  

✅ **These enhancements make TaskMaster a user-friendly, secure, and visually rich task management tool!**

--- 

This version aligns precisely with your notes, including all templates and details as provided, while avoiding extraneous additions like SQL optimization. Let me know if you need further tweaks!