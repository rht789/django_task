from django.urls import path,include
from users.views import signup,sign_in

urlpatterns = [
    path('sign-up/', signup, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
]
