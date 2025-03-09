from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login,logout,authenticate
from users.forms import RegisterForm,CustomRegisterForm, LoginForm, AssignRoleForm, CreateGroupForm
from django.contrib import messages


# Create your views here.
def signup(request):
    if request.method == 'GET':
        form = CustomRegisterForm()
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Prevent immediate save to handle password hashing
            user.set_password(form.cleaned_data.get('password1'))  # Hash the password
            user.is_active = False
            user.save()
            messages.success(request, "A confirmation mail sent, please check your email")
            return redirect('sign-in')
        else:
            print("Form is not valid")
            messages.error(request, "Account Creation failed")
    return render(request, 'registration/register.html', {'form': form})

def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, "registration/signin.html", {'form': form})

def sign_out(request):
    if request.method == 'POST':
        logout(request)
    return redirect('sign-in')

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

def admin_dashboard(request):
    users = User.objects.all()
    return render(request, 'admin/dashboard.html', {'users' : users})
def assign_role(request, user_id):
    user = User.objects.get(id = user_id)
    form = AssignRoleForm()
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request,f'{user.username} has been succefully assigned to the {role.name} role')
            return redirect('admin-dashboard')
    return render(request,'admin/assign_role.html',{'form': form})

def create_group(request):
    form = CreateGroupForm()
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f'{group.name} has been created Succesfully')
            return redirect('admin-dashboard')
    return render(request, 'admin/create_group.html', {'form':form})

def group_list(request):
    groups = Group.objects.all()
    return render(request, 'admin/group_list.html', {'groups':groups})