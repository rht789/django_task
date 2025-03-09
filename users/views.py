from django.shortcuts import redirect, render
from django.contrib.auth.models import User, Group
from django.contrib.auth import login,logout,authenticate
from users.forms import RegisterForm,CustomRegisterForm, AssignRoleForm, CreateGroupForm
from django.contrib import messages


# Create your views here.
def signup(request):
    if request.method == 'GET':
        form = CustomRegisterForm()
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Prevent immediate save to handle password hashing
            user.set_password(form.cleaned_data['password1'])  # Hash the password
            user.save()
            messages.success(request, "Account Created Successfully")
        else:
            print("Form is not valid")
            messages.error(request, "Account Creation failed")
    return render(request, 'registration/register.html', {'form': form})

def sign_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        
        else:
            return render(request,'registration/signin.html', {'error': 'Invalid Username or Password'})
        
    return render(request, "registration/signin.html")

def sign_out(request):
    if request.method == 'POST':
        logout(request)
    return redirect('sign-in')

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