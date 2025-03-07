from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from users.forms import RegisterForm,CustomRegisterForm, LoginForm
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
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login success")
            return redirect('home')
    return render(request, "registration/signin.html", {'form': form})

def sign_out(request):
    if request.method == 'POST':
        logout(request)
    return redirect('sign-in')