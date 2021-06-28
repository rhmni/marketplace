from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from app_account.forms import UserChangeForm, UserCreationForm
from app_account.models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('phone', 'id', 'name', 'is_seller', 'is_superuser', 'is_active')
    list_filter = ('is_superuser', 'is_active', 'is_superuser')
    fieldsets = (
        ('Security information', {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_active', 'is_seller')}),
        ('Important date', {'fields': ('last_update', 'last_login', 'register_date')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'name', 'password1', 'password2'),
        }),
    )
    search_fields = ('phone', 'name')
    ordering = ('-id',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
