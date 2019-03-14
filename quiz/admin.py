from django.contrib import admin
from django.contrib.auth.models import Permission

from quiz.models import Quizzes, Results

admin.site.register(Quizzes)
admin.site.register(Results)
admin.site.register(Permission)
