from django.contrib import admin
from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name',
         'last_name', 'email', 'bio', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Importants Dates', {'fields': ('last_login', 'date_joined')})
    )
    

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('username', 'password1', 'password2', 'email', 'bio', 'profile_image')
        }),
    )
    def profile_image_thumbnail(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="30" height="30" />', obj.profile_image.url)
        return "No Image"
    profile_image_thumbnail.short_description = 'Profile Image'
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'profile_image_thumbnail')

    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)