from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from users.forms import RegisterForm,CustomRegisterForm


# Create your views here.
def signup(request):
    if request.method == 'GET':
        form = CustomRegisterForm()
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print("Form is not valid")
    return render(request, 'registration/register.html', {'form': form})