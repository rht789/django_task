from django.urls import path,include
from users.views import activate_user,CustomLoginView,ProfileView,CustomPasswordChangeView,CustomPasswordChangeDoneView,CustomPasswordResetView,CustomPasswordResetConfirmView,EditProfileView, SignUpView, CustomLogoutView, AdminDashboard,AssignRoleView, CreateGroup,GroupListView


urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    # path('sign-in/', sign_in, name='sign-in'),
    path('sign-in/', CustomLoginView.as_view(), name='sign-in'),
    path('sign-out/', CustomLogoutView.as_view(), name='sign-out'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='change-password'),
    path('admin/dashboard/', AdminDashboard.as_view(), name = 'admin-dashboard'),
    path('admin/<int:user_id>/assign-role/', AssignRoleView.as_view(), name = 'assign-role'),
    path('admin/create-group/', CreateGroup.as_view(), name = 'create-group'),
    path('admin/group-list/', GroupListView.as_view(), name='group-list'),
    path('password-change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='reset-password'),
    path('password-reset/confirm/<uidb64>/<token>/',CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('edit-profile/', EditProfileView.as_view(), name='edit-profile')
]
