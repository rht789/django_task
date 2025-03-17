from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskModelForm, TaskDetailModelForm
from tasks.models import *
from django.db.models import Q, Count, Max, Min
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import ContextMixin

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
@permission_required("tasks.view_task", login_url='no-permission')
def task_details(request, task_id):
    task = Task.objects.get(id=task_id)
    status_choices = Task.STATUS_CHOICES
    if request.method == "POST":
        changed_status = request.POST.get('task_status')
        task.status = changed_status
        task.save()
        return redirect('task_details', task.id)
    return render(request,'task_details.html', {'task':task, 'status_choices' : status_choices})


class CreateTask(ContextMixin,LoginRequiredMixin,PermissionRequiredMixin,View):
    
    login_url='sign-in'
    permission_required='tasks.add_task'
    template_name = 'task_form.html'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["task_form"] = kwargs.get('task_form', TaskModelForm())
        context["task_detail_form"] = kwargs.get('task_detail_form', TaskDetailModelForm())
    
    def get(self,request,*args,**kwargs): 
        context = self.get_context_data()
        return render(request,self.template_name, context) 
    
    def post(self,request,*args,**kwargs):
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
        if task_form.is_valid() and task_detail_form.is_valid():
            """For Django model Form"""
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request, "Task Created Successfully")
            context = self.get_context_data(task_form=task_form, task_detail_form=task_detail_form)
            return render(request,self.template_name, context)  


update_decorators = [login_required,permission_required("tasks.change_task", login_url='no-permission')]

@method_decorator(update_decorators,name='dispatch')

class UpdateClass(View):
    template_name = 'task_form.html'
    def get(self, request, *args, **kwargs):
        task = Task.objects.get(id=id)
        task_form = TaskModelForm(instance=task)
        
        if task.details:
            taskdetail_form = TaskDetailModelForm(instance=task.details)
        context = {
        "task_form" : task_form,
        "taskdetail_form" : taskdetail_form
        }
        return render(request,self.template_name, context)
    def post(self, request, *args, **kwargs):
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

@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect('manager_dashboard')
    elif is_employee(request.user):
        return redirect('employee_dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')

    return redirect('no-permission')