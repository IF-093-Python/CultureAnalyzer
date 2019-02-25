from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Role

admin.site.register(Role)
admin.site.register(Profile)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_staff', 'role')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    list_select_related = ('profile',)

    def role(self, instance):
        role = instance.profile.role.name
        return role

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    role.admin_order_field = 'groups'
