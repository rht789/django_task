from django.urls import path
from tasks.views import show_task,show_specific_task

urlpatterns = [
    path('show_task/', show_task),
    path('show_task/<int:id>', show_specific_task) #jei datatype nibo sheita lekhte hbe routes ey
]