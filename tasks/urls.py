from django.urls import path
from tasks.views import manager_dashboard,employee_dashboard,create_task,view_task,task_details,update_task,delete_task

urlpatterns = [
    # path('show_task/<int:id>', show_specific_task) #jei datatype nibo sheita lekhte hbe routes ey
    path('manager_dashboard/', manager_dashboard, name="manager_dashboard"),
    path('employee_dashboard/', employee_dashboard, name='employee_dashboard' ),
    path('create_task/', create_task, name='create_task'),
    path('view_tasks/', view_task),
    path('task/<int:task_id>/details', task_details, name='task_details'),
    path('update_task/<int:id>', update_task, name='update_task'),
    path('delete_task/<int:id>', delete_task, name='delete_task')
]