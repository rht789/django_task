from django.urls import path,include
from users.views import signup,sign_in,sign_out,admin_dashboard,assign_role,create_group,group_list,activate_user,CustomLoginView,ProfileView,ChangePassword,PasswordChangeDoneView,PasswordReset
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('sign-up/', signup, name='sign-up'),
    # path('sign-in/', sign_in, name='sign-in'),
    path('sign-in/', CustomLoginView.as_view(), name='sign-in'),
    path('sign-out/', LogoutView.as_view(), name='sign-out'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password_change/', ChangePassword.as_view(), name='change-password'),
    path('admin/dashboard/', admin_dashboard, name = 'admin-dashboard'),
    path('admin/<int:user_id>/assign-role/', assign_role, name = 'assign-role'),
    path('admin/create-group/', create_group, name = 'create-group'),
    path('admin/group-list/', group_list, name='group-list'),
    path('password-change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', PasswordReset.as_view(), name='reset-password')
    
]
