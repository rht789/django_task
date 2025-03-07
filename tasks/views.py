from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm, TaskDetailModelForm
from tasks.models import *
from django.db.models import Q, Count, Max, Min
from django.contrib import messages

# Create your views here.
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

def delete_task(request,id):
    if request.method == "POST":
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request,"Task Deleted Successfully")
        return redirect('manager_dashboard')
    messages.error(request,"Something went Wrong")
    redirect("manager_dashboard")

def view_task(request):
    project2 = Project.objects.annotate(task_num = Count("task"))
    return render(request, "view_task.html", {"project2":project2})
