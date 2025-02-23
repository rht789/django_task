from django.contrib import admin
from tasks.models import *

# Register your models here.
admin.site.register(Task)
admin.site.register(TaskDetail)
admin.site.register(Employee)
admin.site.register(Project)