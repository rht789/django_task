from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
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
            user.set_password(form.cleaned_data['password1'])  # Hash the password
            user.save()
            messages.success(request, "Account Created Successfully")
        else:
            print("Form is not valid")
            messages.error(request, "Account Creation failed")
    return render(request, 'registration/register.html', {'form': form})