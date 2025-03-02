from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    #Work with db
    #transform data
    #Data pass
    #http response// json response
    return render(request,'home.html')