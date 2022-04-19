from django.contrib import admin
from .models import MyUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserCreationForm as BaseUserCreationForm


class UserAdmin(BaseUserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'email_verified', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'dob')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'email_verified', 'dob', 'password1', 'password2'),
        }),
    )
    list_display = ('email',)
    search_fields = ('email',)
    ordering = ('email',)


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = MyUser
        fields = ('email', 'email_verified', 'dob')


admin.site.register(MyUser, UserAdmin)
