from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class allUsersAdmin(UserAdmin):
    model = User
    ordering = ['id']
    list_display = ['id', 'username', 'email', 'phone',
                    'gender', 'last_login', 'is_active', 'is_verified']
    list_display_links = []
    # list_editable =['gender']
    search_fields = ['phone', 'username', 'email']
    list_filter = ['gender', 'last_login', 'is_active', 'is_verified']

    fieldsets = [

        ('Authentication Info', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password')
        }),
        ('Personal info', {
            'classes': ('wide',),
            'fields': ('profile_image', 'nationality', 'gender')
        }),
        ('Contact info', {
            'classes': ('wide',),
            'fields': ('phone',)
        }),
        ('Permissions', {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified')
        }),
        ('Important Dates', {
            'classes': ('wide',),
            'fields': ('date_joined', 'last_login')
        }),


    ]


admin.site.register(User, allUsersAdmin)
