from django.urls import path,include
from users.views import signup,sign_in,sign_out,admin_dashboard

urlpatterns = [
    path('sign-up/', signup, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
    path('sign-out/', sign_out, name='sign-out'),
    path('admin/dashboard', admin_dashboard, name = 'admin-dashboard')
]
