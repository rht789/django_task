from django.urls import path,include
from users.views import signup,sign_in,sign_out,activate_user

urlpatterns = [
    path('sign-up/', signup, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
    path('sign-out/', sign_out, name='sign-out'),
    path('activate/<int:user_id>/<str:token>', activate_user),
]
