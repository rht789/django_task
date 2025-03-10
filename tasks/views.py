from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm, TaskDetailModelForm
from tasks.models import *
from django.db.models import Q, Count, Max, Min
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required

# Create your views here.
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_employee(user):
    return user.groups.filter(name='Employee').exists()

@user_passes_test(is_manager, login_url='no-permission')
def manager_dashboard(request):
    type = request.GET.get('type','all')
    base_query=Task.objects.select_related('details').prefetch_related('assigned_to')
    if type=='completed':
        tasks=base_query.filter(status='COMPLETED')
    elif type=='in_progress':
        tasks=base_query.filter(status='IN_PROGRESS')
    elif type=='pending':
        tasks=base_query.filter(status='PENDING')
    else:
        tasks=base_query.all()
    counts = Task.objects.aggregate(
        total_task=Count('id'),
        completed_task=Count('id', filter=Q(status='COMPLETED')),
        in_progress_task=Count('id', filter=Q(status='IN_PROGRESS')),
        pending_task=Count('id', filter=Q(status='PENDING'))
    )
    
    context = {
        "tasks":tasks,
        "counts":counts
    }
    return render(request, "dashboard/manager_dashboard.html",context=context)

@user_passes_test(is_employee, login_url='no-permission')
def employee_dashboard(request):
    return render(request, "dashboard/user_dashboard.html")

@login_required
@permission_required("tasks.add_task", login_url='no-permission')
def create_task(request):
    task_form = TaskModelForm()
    taskdetail_form = TaskDetailModelForm()
    if request.method == "POST":
        task_form = TaskModelForm(request.POST)
        taskdetail_form = TaskDetailModelForm(request.POST)
        if task_form.is_valid() and taskdetail_form.is_valid():
            """For Django model Form"""
            task = task_form.save()
            taskdetail = taskdetail_form.save(commit=False)
            taskdetail.task = task
            taskdetail.save()
            messages.success(request, "Task Created Successfully")
            return redirect('create_task')                
    context = {
        "task_form" : task_form,
        "taskdetail_form" : taskdetail_form
    }
    return render(request,'task_form.html', context)

@login_required
@permission_required("tasks.change_task", login_url='no-permission')
def update_task(request,id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task)
    
    if task.details:
        taskdetail_form = TaskDetailModelForm(instance=task.details)
        
    if request.method == "POST":
        task_form = TaskModelForm(request.POST, instance=task)
        taskdetail_form = TaskDetailModelForm(request.POST, instance=task.details)
        if task_form.is_valid() and taskdetail_form.is_valid():
            """For Django model Form"""
            task = task_form.save()
            taskdetail = taskdetail_form.save(commit=False)
            taskdetail.task = task
            taskdetail.save()
            
            messages.success(request, "Task Updated Successfully")
            return redirect('update_task',id)                
    context = {
        "task_form" : task_form,
        "taskdetail_form" : taskdetail_form
    }
    return render(request,'task_form.html', context)

@login_required
@permission_required("tasks.delete_task", login_url='no-permission')
def delete_task(request,id):
    if request.method == "POST":
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request,"Task Deleted Successfully")
        return redirect('manager_dashboard')
    messages.error(request,"Something went Wrong")
    redirect("manager_dashboard")

@login_required
@permission_required("tasks.view_task", login_url='no-permission')
def view_task(request):
    project2 = Project.objects.annotate(task_num = Count("task"))
    return render(request, "view_task.html", {"project2":project2})
