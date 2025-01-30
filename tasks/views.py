from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    #Work with db
    #transform data
    #Data pass
    #http response// json response
    return HttpResponse("Welcome to the task management system")
def manager_dashboard(request):
    return render(request, "dashboard/manager_dashboard.html")
def user_dashboard(request):
    return render(request, "dashboard/user_dashboard.html")
def test(request):
    return render(request,'test.html')
