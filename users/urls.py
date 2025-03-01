from django.urls import path,include
from users.views import signup

urlpatterns = [
    path('sign-up/', signup, name='sign-up')
]
