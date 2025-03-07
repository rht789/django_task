from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from users.forms import RegisterForm,CustomRegisterForm
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