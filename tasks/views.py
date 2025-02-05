from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm
from tasks.models import *

# Create your views here.
def home(request):
    #Work with db
    #transform data
    #Data pass
    #http response// json response
    return HttpResponse("Welcome to the task management system")
def manager_dashboard(request):
    return render(request, "dashboard/manager_dashboard.html")
def user_dashboard(request):
    return render(request, "dashboard/user_dashboard.html")
def test(request):
    names = ["Rezaul","Karim","Rahat"]
    count = 0
    for name in names:
        count+=1
    context = {
        "names" : names,
        "age" : 23,
        "count" : count
    }
    return render(request,'test.html', context)

def create_task(request):
    employees = Employee.objects.all()
    
    form = TaskForm(employees=employees)
    if request.method == "POST":
        form = TaskForm(request.POST, employees=employees)
        if form.is_valid():
            data = form.cleaned_data
            title = data.get('title')
            description = data.get('description')
            due_date = data.get('due_date')
            assigned_to = data.get('assigned_to')
            task = Task.objects.create(title=title,description=description,due_date=due_date)
            
            for emp_id in assigned_to:
                employee = Employee.objects.get(id=emp_id)
                task.assigned_to.add(employee)
            return HttpResponse("Task Created Succesfully")
    # if request.method == "POST":
    #     form = TaskForm(request.POST,employees=employees)
    #     if form.is_valid():
    #         data = form.cleaned_data
    #         title = data.get("title")
    #         description = data.get("description")
    #         due_date = data.get("due_date")
    #         assigned_to = data.get("assigned_to")
            
    #         task = Task.objects.create(title=title,description=description,due_date=due_date)
            
    #         for emp_id in assigned_to:
    #             emp = Employee.objects.get(id=emp_id)
    #             task.assigned_to.add(emp)
    #         return HttpResponse("Task Created Successfully")
    context = {
        "form" : form
    }
    return render(request,'task_form.html', context)

