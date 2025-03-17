from django.urls import path
from tasks.views import manager_dashboard,employee_dashboard,view_task,task_details,UpdateClass,delete_task,dashboard,CreateTask

urlpatterns = [
    # path('show_task/<int:id>', show_specific_task) #jei datatype nibo sheita lekhte hbe routes ey
    path('manager_dashboard/', manager_dashboard, name="manager_dashboard"),
    path('employee_dashboard/', employee_dashboard, name='employee_dashboard' ),
    path('create_task/', CreateTask.as_view(), name='create_task'),
    path('view_tasks/', view_task),
    path('task/<int:task_id>/details', task_details, name='task_details'),
    path('update_task/<int:id>', UpdateClass.as_view(), name='update_task'),
    path('delete_task/<int:id>', delete_task, name='delete_task'),
    path('dashboard', dashboard, name='dashboard')
]