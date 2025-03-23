from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskModelForm, TaskDetailModelForm
from tasks.models import *
from django.db.models import Q, Count, Max, Min
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, DetailView, UpdateView, TemplateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_employee(user):
    return user.groups.filter(name='Employee').exists()


class ManagerDashboard(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = 'sign-in'
    model = Task
    template_name = "dashboard/manager_dashboard.html"
    context_object_name = 'tasks'
    
    def test_func(self):
        return is_manager(self.request.user)
    
    def get_login_url(self):
        return 'no-permission'
    
    def get_queryset(self):
        type = self.request.GET.get('type','all')
        base_query=Task.objects.select_related('details').prefetch_related('assigned_to')
        if type=='completed':
            return base_query.filter(status='COMPLETED')
        elif type=='in_progress':
            return base_query.filter(status='IN_PROGRESS')
        elif type=='pending':
            return base_query.filter(status='PENDING')
        return base_query.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['counts'] = Task.objects.aggregate(
            total_task=Count('id'),
            completed_task=Count('id', filter=Q(status='COMPLETED')),
            in_progress_task=Count('id', filter=Q(status='IN_PROGRESS')),
            pending_task=Count('id', filter=Q(status='PENDING'))
        )
        return context
    

class EmployeeDashboard(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
    login_url = 'sign-in'
    template_name = "dashboard/user_dashboard.html"
    
    def test_func(self):
        return is_employee(self.request.user)
    
    def get_login_url(self):
        return 'no-permission'
    
class TaskDetails(DetailView,LoginRequiredMixin,PermissionRequiredMixin):
    model = Task
    login_url='sign-in'
    permission_required='tasks.view_task'
    template_name='task_details.html'
    context_object_name='task'
    pk_url_kwarg='task_id'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['status_choices'] = Task.STATUS_CHOICES
        return context
    
    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        changed_status = request.POST.get('task_status')
        self.object.status = changed_status
        self.object.save()
        return redirect('task_details', self.object.id)
        

class CreateTask(ContextMixin,LoginRequiredMixin,PermissionRequiredMixin,View):
    
    login_url='sign-in'
    permission_required='tasks.add_task'
    template_name = 'task_form.html/'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["task_form"] = kwargs.get('task_form', TaskModelForm())
        context["task_detail_form"] = kwargs.get('task_detail_form', TaskDetailModelForm())
        return context
    
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


class UpdateTask(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url='sign-in'
    permission_required='tasks.change_task'
    model = Task
    form_class = TaskModelForm
    template_name = 'task_form.html'
    context_object_name = 'task'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = self.get_form()
        print(context)
        if hasattr(self.object, 'details') and self.object.details:
            context['task_detail_form'] = TaskDetailModelForm(
                instance=self.object.details)
        else:
            context['task_detail_form'] = TaskDetailModelForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_form = TaskModelForm(request.POST, instance=self.object)

        task_detail_form = TaskDetailModelForm(
            request.POST, request.FILES, instance=getattr(self.object, 'details', None))

        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Updated Successfully")
            return redirect('update_task', self.object.id)
        return redirect('update_task', self.object.id)

class DeleteTask(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = Task
    pk_url_kwarg = 'id'
    success_url=reverse_lazy('manager_dashboard')
    
    login_url='sign-in'
    permission_required = "tasks.delete_task"
    def get_permission_denied_url(self):
        return 'no-permission'
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "Task Deleted Successfully")
        return super().delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        messages.error(request, "Something went Wrong")
        return redirect('manager_dashboard')
        

class ViewProject(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = Project  
    login_url = 'sign-in'
    permission_required = "tasks.view_project"
    context_object_name = 'project2'  
    template_name = 'view_task.html' 

    def get_queryset(self):
        queryset = Project.objects.annotate(
            task_num=Count('task')  
        ).order_by('task_num')  
        return queryset

@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect('manager_dashboard')
    elif is_employee(request.user):
        return redirect('employee_dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')

    return redirect('no-permission')