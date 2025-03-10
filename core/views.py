from django.shortcuts import render

# Create your views here.
def home(request):
    #Work with db
    #transform data
    #Data pass
    #http response// json response
    return render(request,'home.html')

def no_permission(request):
    return render(request,'no_permission.html')