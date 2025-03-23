from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login,logout
from users.forms import CustomRegisterForm, LoginForm, AssignRoleForm, CreateGroupForm, CustomPasswordChangeForm,CustomPasswordResetForm,CustomPasswordResetConfirmForm, EditProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordChangeDoneView, PasswordResetView, PasswordResetConfirmView, LogoutView
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, FormView
from users.models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin, UserPassesTestMixin


User = get_user_model()

class EditProfileView(UpdateView):
    model = CustomUser
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save(commit=True)
        return redirect('profile')

def is_admin(user):
    return user.is_authenticated and user.groups.filter(name='Admin').exists()


class SignUpView(AccessMixin, CreateView):
    model = User
    form_class = CustomRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('sign-in')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password1'))
        user.is_active = False
        user.save()
        messages.success(self.request, "A confirmation mail sent, please check your email")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Account Creation failed")
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    form_class=LoginForm
    template_name='registration/signin.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()

class CustomLogoutView(LoginRequiredMixin,LogoutView):
    login_url='sign-in'
    

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id = user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')
    except user.DoesNotExist:
        return HttpResponse('User not found')


class AdminDashboard(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = 'sign-in'
    model = User
    template_name = "admin/dashboard.html"
    context_object_name = 'users'
    
    def test_func(self):
        return is_admin(self.request.user)
    
    def get_login_url(self):
        return 'no-permission'
    
    def get_queryset(self):
        queryset = User.objects.prefetch_related(Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')).all()

        for user in queryset:
            if user.all_groups:
                user.group_name = user.all_groups[0].name
            else:
                user.group_name = 'No Group Assigned'
        return queryset


class AssignRoleView(UserPassesTestMixin, FormView):
    template_name = 'admin/assign_role.html'
    form_class = AssignRoleForm
    success_url = reverse_lazy('admin-dashboard')

    def test_func(self):
        return is_admin(self.request.user)

    def get_login_url(self):
        return 'no-permission'

    def get_user(self):
        return User.objects.get(id=self.kwargs['user_id'])

    def form_valid(self, form):
        user = self.get_user()
        role = form.cleaned_data.get('role')
        user.groups.clear()
        user.groups.add(role)
        messages.success(self.request, f'{user.username} has been successfully assigned to the {role.name} role')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.get_user()
        return context


class CreateGroup(UserPassesTestMixin,CreateView):
    model=Group
    form_class=CreateGroupForm
    template_name='admin/create_group.html'
    
    
    def test_func(self):
        return is_admin(self.request.user)

    def get_login_url(self):
        return 'no-permission'
    
    def form_valid(self, form):
        group = form.save()
        messages.success(self.request, f'{group.name} has been created Succesfully')
        return super().form_valid(form)
    

class GroupListView(UserPassesTestMixin,ListView):
    model=Group
    template_name='admin/group_list.html'
    context_object_name = 'groups'
    
    def test_func(self):
        return is_admin(self.request.user)

    def get_login_url(self):
        return 'no-permission'
    
    def get_queryset(self):
        return Group.objects.prefetch_related('permissions').all()

class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        user = self.request.user
        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['bio'] = user.bio
        context['profile_image'] = user.profile_image
        
        context['date_joined'] = user.date_joined
        context['last_login']= user.last_login
        
        return context
    
class CustomPasswordChangeView(PasswordChangeView):
    form_class=CustomPasswordChangeForm
    template_name='accounts/password_change.html'
    
class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name='accounts/password_change_done.html'
    
class CustomPasswordResetView(PasswordResetView):
    form_class=CustomPasswordResetForm
    template_name='registration/reset_password.html'
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'registration/reset_email.html'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context

    def form_valid(self, form):
        messages.success(
        self.request, 'A Reset email sent. Please check your email')
        return super().form_valid(form)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class=CustomPasswordResetConfirmForm
    template_name='registration/reset_password.html'
    success_url = reverse_lazy('sign-in')

    
    def form_valid(self, form):
        messages.success(
        self.request, 'Password Reset Successfully!')
        return super().form_valid(form)
