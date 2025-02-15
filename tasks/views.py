from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm
from tasks.models import *
from django.db.models import Q, Count, Max, Min

# Create your views here.
def home(request):
    #Work with db
    #transform data
    #Data pass
    #http response// json response
    return HttpResponse("Welcome to the task management system")
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
    print(type)
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
    form = TaskModelForm()
    if request.method == "POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():
            """For Django model Form"""
            # form.save()
            # return HttpResponse("Task Created Succesfully")
            return render(request, 'task_form.html', {'form':form, 'message':'task created successsfully'})

            
    
            """For Django Form Data"""
            #         data = form.cleaned_data
            #         title = data.get('title')
            #         description = data.get('description')
            #         due_date = data.get('due_date')
            #         assigned_to = data.get('assigned_to')
            #         task = Task.objects.create(title=title,description=description,due_date=due_date)
                    
            #         for emp_id in assigned_to:
            #             employee = Employee.objects.get(id=emp_id)
            #             task.assigned_to.add(employee)
                    
    context = {
        "form" : form
    }
    return render(request,'task_form.html', context)

def view_task(request):
    project2 = Project.objects.annotate(task_num = Count("task"))
    return render(request, "view_task.html", {"project2":project2})
