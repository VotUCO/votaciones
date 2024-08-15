from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

# Register your models here.
@admin.register(User)
class UsersAdmin(UserAdmin):
    fieldsets= (
        (None, {
            'fields': ('username', 'email')
        }),
        ('Información Extra',{
            'fields': ('birth_date', 'gender')
        }),
        ('Permisos', {
            'fields': ('is_superuser', 'is_staff', 'groups')
        })
    )