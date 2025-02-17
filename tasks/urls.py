from django.urls import path
from tasks.views import *

urlpatterns = [
    # path('show_task/<int:id>', show_specific_task) #jei datatype nibo sheita lekhte hbe routes ey
    path('manager_dashboard/', manager_dashboard, name="manager_dashboard"),
    path('user_dashboard/', user_dashboard),
    path('test/', test),
    path('create_task/', create_task, name='create_task'),
    path('view_tasks/', view_task),
    path('update_task/<int:id>', update_task, name='update_task')
]