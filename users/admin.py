from django.contrib import admin

from .models import Profile, Role

admin.site.register(Role)
admin.site.register(Profile)
