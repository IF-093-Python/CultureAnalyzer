from django.contrib import admin

from .models import Profile, Role, CustomUser

admin.site.register([CustomUser, Role, Profile])
