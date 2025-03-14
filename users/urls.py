from django.urls import path,include
from users.views import signup,sign_in,sign_out,admin_dashboard,assign_role,create_group,group_list,activate_user

urlpatterns = [
    path('sign-up/', signup, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
    path('sign-out/', sign_out, name='sign-out'),
    path('activate/<int:user_id>/<str:token>', activate_user),
    path('admin/dashboard', admin_dashboard, name = 'admin-dashboard'),
    path('admin/<int:user_id>/assign-role/', assign_role, name = 'assign-role'),
    path('admin/create-group/', create_group, name = 'create-group'),
    path('admin/group-list/', group_list, name='group-list')
]
