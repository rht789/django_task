from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    #Work with db
    #transform data
    #Data pass
    #http response// json response
    return HttpResponse("Welcome to the task management system")
def contact(request):
     return HttpResponse("<h1 style = 'color : red'>This is Contact</h1> <br> Hi")
# must use single quotation inside double quotation

def show_task(request):
    return HttpResponse("This is our task")
def show_specific_task(request,id):
    return HttpResponse(f'This is our task no. {id}')