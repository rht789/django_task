from django.contrib import admin
from django.urls import path,include
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import home


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name='home'),
    path("tasks/", include("tasks.urls")),
    path("users/", include("users.urls"))
] + debug_toolbar_urls()
