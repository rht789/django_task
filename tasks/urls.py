from django.urls import path
from tasks.views import *

urlpatterns = [
    # path('show_task/<int:id>', show_specific_task) #jei datatype nibo sheita lekhte hbe routes ey
    path('dashboard/', manager_dashboard),
    path('user_dashboard/', user_dashboard),
    path('test/', test),
    path('forms/', forms) 
]